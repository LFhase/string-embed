import os
from enum import Enum
import json
import torch


class Constants:
    Tag_Start = "<START>"
    Tag_End = "<STOP>"
    Tag_Pad = "<T_PAD>"
    Word_Pad = "[PAD]"
    Word_Unknown = "<UNK>"
    Word_End = "<EOF>"
    Char_Pad = "<C_PAD>"
    Char_Unknown = "<C_UNK>"
    Invalid_Transition = -10000
    Models_Folder = "./saved/"
    Logs_Folder = "./logs/"
    Eval_Folder = "./evaluation/"
    Eval_Temp_Folder = os.path.join(Eval_Folder, "tmp")
    Eval_Script = os.path.join(Eval_Folder, "eval.pl")
    BertCache_Folder = "./saved/bert/"


class EnumEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj.name)
        elif isinstance(obj, torch.device):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class LabellingSchema(Enum):
    IOB1 = 0
    IOB2 = 1
    IOBES = 2


class CharEmbeddingSchema(Enum):
    CNN = 1
    LSTM = 2


class OptimizationMethod(Enum):
    SGDWithDecreasingLR = 1
    AdaDelta = 2
    Adam = 3


class ActivationFunction(Enum):
    ReLu = 1
    Tanh = 2


class PretrainedModelChoice(Enum):
    #TODO: too many chocies here, need to figure out a right way
    pass


class SchedulerChoice(Enum):
    Exponential = 1
    Linear = 2
    InverseSquareRoot = 3
