import torch
import torch.nn as nn
import pandas as pd
import numpy as np


class xyFeature(object):
    def __init__(self, df, cat_cols, cont_cols, y_col, gpu=False):
        self.df = df.dropna()
        self.cat_cols = cat_cols
        self.cont_cols = cont_cols
        self.y_col = y_col
        self.gpu = gpu

    def prepare_XY(self):
        if self.gpu:
            self.df[self.y_col] = self.df[self.y_col].astype('category')
            y = np.stack([self.df[col].cat.codes.values for col in self.y_col], 1)
            y = torch.tensor(y, dtype=torch.long).flatten().cuda()

            for cat in self.cat_cols:
                self.df[cat] = self.df[cat].astype('category')

            cats = np.stack([self.df[col].cat.codes.values for col in self.cat_cols], 1)
            cats = torch.tensor(cats, dtype=torch.int64).cuda()
            

            conts = np.stack([self.df[col].values for col in self.cont_cols], 1)
            conts = torch.tensor(conts, dtype=torch.float).cuda()
        else:
            self.df[self.y_col] = self.df[self.y_col].astype('category')
            y = np.stack([self.df[col].cat.codes.values for col in self.y_col], 1)
            y = torch.tensor(y, dtype=torch.long).flatten()

            for cat in self.cat_cols:
                self.df[cat] = self.df[cat].astype('category')

            cats = np.stack([self.df[col].cat.codes.values for col in self.cat_cols], 1)
            cats = torch.tensor(cats, dtype=torch.int64)
            

            conts = np.stack([self.df[col].values for col in self.cont_cols], 1)
            conts = torch.tensor(conts, dtype=torch.float)

        return cats, conts, y

    def get_size(self):
        _, conts, y = self.prepare_XY()

        cat_szs = [len(self.df[col].cat.categories) for col in self.cat_cols]
        emb_szs = [(size, min(50, (size+1)//2)) for size in cat_szs]

        return emb_szs, conts.shape[1], len(y.unique())

