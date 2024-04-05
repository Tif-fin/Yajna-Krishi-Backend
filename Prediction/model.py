
import torch
from torch_geometric_temporal.nn.attention.stgcn import STConv

class STGCN_Best_BRC(torch.nn.Module):
    def __init__(self):
        super(STGCN_Best_BRC, self).__init__()
        self.stconv_block1 = STConv(750, 18, 64, 128, 9, 4)
        self.stconv_block2 = STConv(750, 128, 256, 64, 7, 4)
        self.stconv_block3 = STConv(750, 64, 32, 16, 5, 3)
        self.fc = torch.nn.Linear(16, 7)
        
    def forward(self, x, edge_index, edge_attr):
        temp = self.stconv_block1(x, edge_index, edge_attr)
        temp = self.stconv_block2(temp, edge_index, edge_attr)
        temp = self.stconv_block3(temp, edge_index, edge_attr)
        temp = self.fc(temp)
        
        return temp
