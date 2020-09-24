import torch
import torch.nn as nn
import pandas as pd
import numpy as np

class MLP(nn.Module):
    def __init__(self, emb_szs, n_cont, out_sz, layers, p=0.5):
        super().__init__()
        self.embeds = nn.ModuleList([nn.Embedding(i,f) for i, f in emb_szs])
        self.emb_drop = nn.Dropout(p)
        self.bn_count = nn.BatchNorm1d(n_cont)
        
        layer_list = []
        n_emb = sum((f for i,f in emb_szs))
        n_input = n_emb + n_cont
        
        for i in layers:
            layer_list.append(nn.Linear(n_input, i))
            layer_list.append(nn.ReLU(inplace=True))
            layer_list.append(nn.BatchNorm1d(i))
            layer_list.append(nn.Dropout(p))
            n_input = i
        layer_list.append(nn.Linear(layers[-1], out_sz)) # output layer
        self.layer = nn.Sequential(*layer_list)
        
    def forward(self, x_cat, x_cont):
        embeddings = []
        for i, e in enumerate(self.embeds):
            embeddings.append(e(x_cat[:,i]))
        x = torch.cat(embeddings, 1)
        x = self.emb_drop(x)
        
        x_cont = self.bn_count(x_cont)
        x = torch.cat([x, x_cont], 1)
        x = self.layer(x)
        return nn.Softmax(dim=1)(x)