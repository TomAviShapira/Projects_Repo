<<<<<<< HEAD
import torch
import torch.nn as nn


class EncoderModel(nn.Module):  # was class dsTCNModel(Base)
    def __init__(self,
                 n_inputs_ch=1,
                 nblocks=12,  # was 13
                 kernel_size=15,
                 stride=2,
                 dilation=1,
                 norm_type='BatchNorm',
                 act_type='PReLU'):
        super(EncoderModel, self).__init__()
        # self.save_hyperparameters()

        self.EncoderFlatten = torch.nn.Flatten()
        self.EncoderAdaptiveAvgPool1d = torch.nn.AdaptiveAvgPool1d(512)
        self.EncoderLinear1 = torch.nn.Linear(512, 384)
        self.EncoderLinear2 = torch.nn.Linear(384, 256)
        self.EncoderLinear3 = torch.nn.Linear(256, 128)

        self.blocks = torch.nn.ModuleList()
        for n in range(nblocks):
            in_ch = n_inputs_ch if n == 0 else out_ch
            if n == 0:
                out_ch = 8
            elif n % 2 == 0:
                out_ch = in_ch * 2
            else:
                out_ch = in_ch

            self.blocks.append(EncoderBlock(
                in_ch,
                out_ch,
                kernel_size,
                stride,
                dilation,
                norm_type,
                act_type
            ))

    def forward(self, x):

        for block in self.blocks:
            x = block(x)

        x = self.EncoderFlatten(x)
        # x = x.unsqueeze(0)
        x = self.EncoderAdaptiveAvgPool1d(x)
        x = self.EncoderLinear1(x)
        x = self.EncoderLinear2(x)
        x = self.EncoderLinear3(x)

        return x


class EncoderBlock(torch.nn.Module):
    def __init__(self,
                 in_ch,
                 out_ch,
                 kernel_size,
                 stride=1,
                 dilation=1,
                 norm_type=None,
                 act_type="PReLU"):
        super(EncoderBlock, self).__init__()
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.kernel_size = kernel_size
        self.stride = stride
        self.norm_type = norm_type

        pad_value = ((kernel_size - 1) * dilation) // 2

        self.conv1 = torch.nn.Conv1d(in_ch,
                                     out_ch,
                                     kernel_size=kernel_size,
                                     stride=stride,
                                     dilation=dilation,
                                     padding=pad_value)
        self.act1 = get_activation(act_type, out_ch)

        if norm_type == "BatchNorm":
            self.norm1 = torch.nn.BatchNorm1d(out_ch)
            # self.norm2 = torch.nn.BatchNorm1d(out_ch)
            self.res_norm = torch.nn.BatchNorm1d(out_ch)
        else:
            self.norm1 = None
            self.res_norm = None

        # self.conv2 = torch.nn.Conv1d(out_ch,
        #                             out_ch,
        #                             kernel_size=1,
        #                             stride=1)
        # self.act2 = get_activation(act_type, out_ch)

        self.res_conv = torch.nn.Conv1d(in_ch,
                                        out_ch,
                                        kernel_size=1,
                                        stride=stride)

    def forward(self, x):
        x_res = x  # store input for later

        # -- first section --
        x = self.conv1(x)
        if self.norm1 is not None:
            x = self.norm1(x)
        x = self.act1(x)

        # -- second section --
        # x = self.conv2(x)
        # if self.norm_type is not None:
        #    x = self.norm2(x)
        # x = self.act2(x)

        # -- residual connection --
        x_res = self.res_conv(x_res)
        if self.res_norm is not None:
            x_res = self.res_norm(x_res)

        return x + x_res


def get_activation(act_type,
                   ch=None):
    """ Helper function to construct activation functions by a string.
    Args:
        act_type (str): One of 'ReLU', 'PReLU', 'SELU', 'ELU'.
        ch (int, optional): Number of channels to use for PReLU.

    Returns:
        torch.nn.Module activation function.
    """

    if act_type == "PReLU":
        return torch.nn.PReLU(ch)
    elif act_type == "ReLU":
        return torch.nn.ReLU()
    elif act_type == "SELU":
        return torch.nn.SELU()
    elif act_type == "ELU":
        return torch.nn.ELU()
=======
import torch
import torch.nn as nn


class EncoderModel(nn.Module):  # was class dsTCNModel(Base)
    def __init__(self,
                 n_inputs_ch=1,
                 nblocks=12,  # was 13
                 kernel_size=15,
                 stride=2,
                 dilation=1,
                 norm_type='BatchNorm',
                 act_type='PReLU'):
        super(EncoderModel, self).__init__()
        # self.save_hyperparameters()

        self.EncoderFlatten = torch.nn.Flatten()
        self.EncoderAdaptiveAvgPool1d = torch.nn.AdaptiveAvgPool1d(512)
        self.EncoderLinear1 = torch.nn.Linear(512, 384)
        self.EncoderLinear2 = torch.nn.Linear(384, 256)
        self.EncoderLinear3 = torch.nn.Linear(256, 128)

        self.blocks = torch.nn.ModuleList()
        for n in range(nblocks):
            in_ch = n_inputs_ch if n == 0 else out_ch
            if n == 0:
                out_ch = 8
            elif n % 2 == 0:
                out_ch = in_ch * 2
            else:
                out_ch = in_ch

            self.blocks.append(EncoderBlock(
                in_ch,
                out_ch,
                kernel_size,
                stride,
                dilation,
                norm_type,
                act_type
            ))

    def forward(self, x):

        for block in self.blocks:
            x = block(x)

        x = self.EncoderFlatten(x)
        # x = x.unsqueeze(0)
        x = self.EncoderAdaptiveAvgPool1d(x)
        x = self.EncoderLinear1(x)
        x = self.EncoderLinear2(x)
        x = self.EncoderLinear3(x)

        return x


class EncoderBlock(torch.nn.Module):
    def __init__(self,
                 in_ch,
                 out_ch,
                 kernel_size,
                 stride=1,
                 dilation=1,
                 norm_type=None,
                 act_type="PReLU"):
        super(EncoderBlock, self).__init__()
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.kernel_size = kernel_size
        self.stride = stride
        self.norm_type = norm_type

        pad_value = ((kernel_size - 1) * dilation) // 2

        self.conv1 = torch.nn.Conv1d(in_ch,
                                     out_ch,
                                     kernel_size=kernel_size,
                                     stride=stride,
                                     dilation=dilation,
                                     padding=pad_value)
        self.act1 = get_activation(act_type, out_ch)

        if norm_type == "BatchNorm":
            self.norm1 = torch.nn.BatchNorm1d(out_ch)
            # self.norm2 = torch.nn.BatchNorm1d(out_ch)
            self.res_norm = torch.nn.BatchNorm1d(out_ch)
        else:
            self.norm1 = None
            self.res_norm = None

        # self.conv2 = torch.nn.Conv1d(out_ch,
        #                             out_ch,
        #                             kernel_size=1,
        #                             stride=1)
        # self.act2 = get_activation(act_type, out_ch)

        self.res_conv = torch.nn.Conv1d(in_ch,
                                        out_ch,
                                        kernel_size=1,
                                        stride=stride)

    def forward(self, x):
        x_res = x  # store input for later

        # -- first section --
        x = self.conv1(x)
        if self.norm1 is not None:
            x = self.norm1(x)
        x = self.act1(x)

        # -- second section --
        # x = self.conv2(x)
        # if self.norm_type is not None:
        #    x = self.norm2(x)
        # x = self.act2(x)

        # -- residual connection --
        x_res = self.res_conv(x_res)
        if self.res_norm is not None:
            x_res = self.res_norm(x_res)

        return x + x_res


def get_activation(act_type,
                   ch=None):
    """ Helper function to construct activation functions by a string.
    Args:
        act_type (str): One of 'ReLU', 'PReLU', 'SELU', 'ELU'.
        ch (int, optional): Number of channels to use for PReLU.

    Returns:
        torch.nn.Module activation function.
    """

    if act_type == "PReLU":
        return torch.nn.PReLU(ch)
    elif act_type == "ReLU":
        return torch.nn.ReLU()
    elif act_type == "SELU":
        return torch.nn.SELU()
    elif act_type == "ELU":
        return torch.nn.ELU()
>>>>>>> 0f8de6e6fdc9bfbddd2c211fd16cb0571793da57
