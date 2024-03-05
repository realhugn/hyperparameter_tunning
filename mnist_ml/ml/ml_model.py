import torch as torch
import torch.nn as nn
    
class classicationmodel(nn.Module):
    def __init__(self):
        super( classicationmodel,self).__init__()
        self.linear1 = nn.Linear(28*28, 128) 
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(128, 64) 
        self.relu2 = nn.ReLU()
        self.final = nn.Linear(64, 10)


    def forward(self, image):
        a = image.view(-1, 28*28)
        a = self.linear1(a)
        a = self.relu1(a)
        a = self.linear2(a)
        a = self.relu2(a)
        a = self.final(a)
        return a