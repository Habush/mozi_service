__author__ = 'Abdulrahman Semrie'
import time
import os
import subprocess
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from pathlib import Path
from cross_val.random_seed import RandomSeed
import re
from config import EXPORT_SCRIPT
from models import Task, Result
from utils.moses_res_parser import parse_moses_result

default_list = "-j8 --balance=1 -m 1000 -W1 --output-cscore=1 --result-count 100 --reduct-knob-building-effort=1 --hc-widen-search=1 --enable-fs=1 --fs-algo=smd --fs-target-size=4 --hc-crossover-min-neighbors=5000 --fs-focus=all --fs-seed=init --complexity-ratio=1 --hc-fraction-of-nn=.3 --hc-crossover-pop-size=1000"

table = {'feature-selection': 'fs', 'algorithm': 'algo'}
regex = re.compile(r'(?!^)(?<!_)([A-Z])')
pattern = re.compile(r'\b(' + '|'.join(list(table.keys())) + r')\b')

RESULT_FOLDER = os.path.join(Path(__file__).parent.absolute(), 'data')

def parse_options(opts):
    """
    A function to parse the MOSES options, which is a JSON string, into MOSES commandline options
    :param opts: The MOSES opts in JSON string format
    :return:
    """
    final_opts = "-W1 "
    final_opts += '-j' + str(opts['numberOfThreads'])
    final_opts += ' -m ' + str(opts['maximumEvals'])
    del opts['numberOfThreads']
    del opts['maximumEvals']

    for k, v in list(opts.items()):
        new_k = "--" + camel_case_converter(k)
        val = v
        if isinstance(v, bool):
            if v:
                val = "1"
            else:
                val = "0"

        res = " '{0}={1}' ".format(new_k, val)
        final_opts += res

    result = pattern.sub(lambda x: table[x.group()], final_opts)
    return result


def camel_case_converter(str):
    return regex.sub(r'-\1', str).lower()


class CrossValidation:
    def __init__(self, db, task_id,options, cwd=None):

        print(os.getcwd())
        if cwd is None:
            if not os.path.exists(RESULT_FOLDER):
                os.makedirs(RESULT_FOLDER)

            os.chdir(RESULT_FOLDER)
            os.chdir(task_id)

            if (not os.path.exists(task_id)):
                os.mkdir(task_id)
                os.chdir(task_id)

        else:
            os.chdir(cwd)



        self.db = db
        self.id = task_id
        self.output = self.id
        self.file = os.path.join(os.getcwd(), task_id+".csv")

        moses_opts = options["mosesOptions"]
        cross_val_opts = options["crossValidationOptions"]

        print(options)

        if moses_opts:
            self.category = moses_opts['inputCategory']
            del moses_opts['inputCategory']
            self.opts = parse_options(moses_opts)
        else:
            self.opts = default_list
            self.category = "older-than"

        self.test_size = cross_val_opts["testSize"]

        self.threshold = 50.0

        nsplits = cross_val_opts["folds"]

        self.num_rand_seeds = cross_val_opts["randomSeed"]

        self.dataset = None

        self.cv = StratifiedShuffleSplit(n_splits=nsplits, test_size=self.test_size)

        self.test = []

        self.train_file, self.test_file = "train_temp_" + self.id, "test_temp_" + self.id

        self.results = []

    def run_eval(self):
        temp_out = "eval_" + self.id

        cmd = "eval-table -i {0} -C {1} -o {2} -u{3}".format(self.test_file, self.output, temp_out, "case")
        print(cmd)
        ret = subprocess.Popen(args=cmd, shell=True).wait()
        return ret

    def build_matrix(self):
        files = list(Path(".").glob("eval_" + self.id + "[0-9]*"))

        matrix = np.array([np.genfromtxt(files[i].name, dtype=int, delimiter="\n", skip_header=1) for i in
                           range(len(files))]).T  # transpose the matrix

        for file in files: os.remove(file.name)

        return matrix

    def reduce_matrix(self):
        matrix = self.build_matrix()
        return np.array(
            [1 if ((matrix[i].sum() / matrix.shape[1]) * 100) > self.threshold else 0 for i in range(matrix.shape[0])])

    def score(self):
        scores = self.reduce_matrix()

        print(scores)

        print(len(scores))

        true_positive, true_negative, false_postive, false_negative = 0, 0, 0, 0

        for i in range(len(scores)):
            if self.test.iloc[i] == 0:
                if scores[i] == 0:
                    true_negative += 1
                else:
                    false_postive += 1

            else:
                if scores[i] == 1:
                    true_positive += 1
                else:
                    false_negative += 1

        recall = (true_positive / (true_positive + false_negative)) * 100

        precision = (true_positive / (true_positive + false_postive)) * 100

        accuracy = ((true_positive + true_negative) / (
            true_positive + true_negative + false_negative + false_postive)) * 100

        return recall, precision, accuracy

    def run_cross_val(self):

        try:
            self.dataset = pd.read_csv(self.file)

        except Exception as e:
            Task.update_status(self.db, self.id, -1)
            raise e

        x, y = self.dataset.values, self.dataset.case

        i = 0

        for train_index, test_index in self.cv.split(x, y):
            x_train, x_test = x[train_index], x[test_index]

            self.output = "{0}_fold_{1}".format(self.id, str(i))

            self.test = y[test_index]

            pd.DataFrame(x_train, columns=self.dataset.columns.values).to_csv(self.train_file, index=False)

            pd.DataFrame(x_test, columns=self.dataset.columns.values).to_csv(self.test_file, index=False)

            randSeed = RandomSeed(self.train_file, self.id, i, self.opts, num_rands=self.num_rand_seeds)

            try:
                randSeed.run()

            except ChildProcessError as e:
                Task.update_status(self.db, self.id, -1)
                raise e

            ret = self.run_eval()

            if ret != 0:
                Task.update_status(self.db, self.id, -1)
                raise ChildProcessError("Eval-table error")


            rec, pre, acc = self.score()

            self._build_result(i, rec, pre, acc)

            i += 1

        self.score_ensemble()

        Task.update_status(self.db, self.id, 0) #Task completed successfully

    def _build_result(self, fold, rec, prec, acc):
        # Add the code to instantiate result object after converting them to a scm file

        scm_file = self.output + ".scm"
        cmd = EXPORT_SCRIPT + " {0} '{1}' > {2}".format(self.output, self.category, scm_file)

        ret = subprocess.Popen(args=cmd, shell=True).wait()

        if ret == 0:
            data = parse_moses_result(scm_file)

            rec = "%.2f" % rec
            prec = "%.2f" % prec
            acc = "%.2f" % acc

            result = Result(self.db, self.id, fold, prec, rec, acc, data)
            result.save()

            self.results.append(result)

        else:
            Task.update_status(self.db, self.id, -1)
            raise ChildProcessError("Export script failed")


    def score_ensemble(self):
        path = Path(os.getcwd())

        folds = list(path.glob("*"))
        match = re.compile(".+_fold_[0-9]+$").match

        ensemble_model = []

        for fold in folds:
            if match(fold.name):
                with open(fold.name, 'r') as f:
                    for line in f:
                        ensemble_model.append(line)


        ensemble_file = self.id

        with open(ensemble_file, 'w') as f:
            for model in ensemble_model:
                f.write(model)


        #Score on the ensemble on the whole database
        self.test_file = self.file
        self.test = pd.read_csv(self.file)["case"]

        self.output = ensemble_file

        ret = self.run_eval()

        if ret != 0:
            Task.update_status(self.db, self.id, -1)
            raise ChildProcessError("Eval-table error")

        recall, precision, acc = self.score()

        self._build_result(-1, recall, precision, acc)
