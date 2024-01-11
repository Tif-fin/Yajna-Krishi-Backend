import torch 
from torch_geometric_temporal.nn.attention.stgcn import STConv

class STGCN(torch.nn.Module):
    def __init__(self):
        super(STGCN, self).__init__()
        self.stconv_block1 = STConv(210, 14, 64, 128, 9, 3)
        self.stconv_block2 = STConv(210, 128, 64, 16, 5, 3)
        # self.stconv_block3 = STConv(210, 32, 16, 8, 3, 3)
        self.fc = torch.nn.Linear(16, 3)
        
    def forward(self, x, edge_index, edge_attr):
        temp = self.stconv_block1(x, edge_index, edge_attr)
        temp = self.stconv_block2(temp, edge_index, edge_attr)
        # temp = self.stconv_block3(temp, edge_index, edge_attr)
        temp = self.fc(temp)
        
        return temp
