import torch 
from torch_geometric_temporal.nn.attention.stgcn import STConv



class STGCN(torch.nn.Module):
    """
    Processes a sequence of graph data to produce a spatio-temporal embedding
    to be used for regression, classification, clustering, etc.
    """
    def __init__(self):
        super(STGCN, self).__init__()
        self.stconv_block1 = STConv(210, 9, 18, 32, 2, 4)
        self.stconv_block2 = STConv(210, 32, 18, 9, 2, 4)
        self.fc = torch.nn.Linear(9, 4)
        
    def forward(self, x, edge_index, edge_attr):
        temp = self.stconv_block1(x, edge_index)
        temp = self.stconv_block2(temp, edge_index)
        temp = self.fc(temp)
        
        return temp

model = STGCN()
# model.load_weight('weights.pth')
weight = torch.load('static/Model_60Lags_STConv_Best_Feb18.pt')

model.load_state_dict(weight)

model.predict()



