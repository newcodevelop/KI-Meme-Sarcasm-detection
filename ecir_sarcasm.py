# -*- coding: utf-8 -*-
"""ecir_sarcasm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G9Mnz-BxrNjVVbpf6e3HLNmNfOm8m82r
"""

!pip install NRCLex
!python -m textblob.download_corpora
!pip install ftfy regex tqdm
!pip install git+https://github.com/openai/CLIP.git
!pip install keras_ocr

!pip install pytorch-lightning

# !pip install easyocr

from google.colab import drive
drive.mount('/content/drive')

!pwd

import pandas as pd
# data = pd.read_csv('/content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/MEMES_MY_DATASET_WITHOUT_OVERSAMPLING_new.csv')

# from PIL import Image
# Image.open('/content/drive/MyDrive/memes_our_dataset_hindi/my_meme_data/babies100.png')

# data.head(10)

# data.keys()

# K = pd.DataFrame({'Name':list(data['Name']),
#      'text':list(data['text']),
#      'Sarcasm':list(data['Sarcasm']),
#      'Fear':list(data['Fear']),
#      'Neglect':list(data['Neglect']),
#      'irritation':list(data['irritation']),
#      'Rage':list(data['Rage']),
#      'Disgust':list(data['Disgust']),
#      'Nervousness':list(data['Nervousness']),
#      'Shame':list(data['Shame']),
#      'Disappointment':list(data['Disappointment']),
#      'Envy':list(data['Envy']),
#      'Suffering':list(data['Suffering']),
#      'Sadness':list(data['Sadness']),
#      'Joy':list(data['Joy']),
#      'Pride':list(data['Pride'])})

# K

# K.to_csv('dataset_ecir.csv')

data = pd.read_csv('./dataset_ecir.csv')

data.head(10)

import matplotlib.pyplot as plt
import keras_ocr
import cv2
import math
import numpy as np

import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from tqdm.notebook import tqdm
import clip
from PIL import Image

#!tar -xf /content/logs.tar.gz

!git clone https://github.com/FreddeFrallan/Multilingual-CLIP

!bash Multilingual-CLIP/legacy_get-weights.sh

!pip install transformers

# Commented out IPython magic to ensure Python compatibility.
"""
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
"""

!cp -r /content/data /content/Multilingual-CLIP/
# %cd Multilingual-CLIP
from multilingual_clip import legacy_multilingual_clip
text_model = legacy_multilingual_clip.load_model('M-BERT-Distil-40')
# %cd ..
!pwd

#sample = data['text'][0]

#sample

#text_model(sample)



device = 'cuda' if torch.cuda.is_available() else 'cpu'
clip_model, compose = clip.load('RN50x4', device = device)

text_model = text_model.cpu()

def process(idx_val,arr):
  if idx_val=='0':
    arr.append(0)
  else:
    arr.append(1)

def get_data(data):
  #data = pd.read_csv(dataset_path)
  text = list(data['text'])
  img_path = list(data['Name'])
  
  Fear = list(data['Fear'])
  Neglect	= list(data['Neglect'])
  irritation=list(data['irritation'])	
  Rage	= list(data['Rage'])
  Disgust	= list(data['Disgust'])
  Nervousness	= list(data['Nervousness'])
  Shame	= list(data['Shame'])
  Disappointment = list(data['Disappointment'])	
  Envy	= list(data['Envy'])
  Suffering	= list(data['Suffering'])
  Sadness	= list(data['Sadness'])
  Joy	= list(data['Joy'])
  Pride = list(data['Pride'])
  Sarcasm = list(data['Sarcasm'])
  
  #optimize memory for features
  name, text_features,image_features, fe, neg, ir, ra, disg, ner, sh, disa, en, su, sa, jo, pr, sar= [],[],[],[],[], \
  [],[],[],[],[],[],[],[],[],[],[],[]
  for txt,img_name,fear,neglect,irritation,rage,disgust,nervousness, shame,disappointment,envy,suffering,sadness,joy,pride, \
  sarcasm \
   in tqdm(zip(text,img_path, Fear,	Neglect,	irritation,	Rage,	Disgust,	\
              Nervousness,	Shame,	Disappointment,	Envy,	Suffering,	Sadness, Joy,	Pride, Sarcasm)):
    
    try:
      img = preprocess(Image.open('/content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/my_meme_data/'+img)).unsqueeze(0).to(device)
      #name.append(img)
      #img = Image.open('/content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/my_meme_data/'+img_name)
      # img = Image.fromarray(inpaint_text('/content/drive/MyDrive/memes_our_dataset_hindi/my_meme_data/'+img_name,pipeline), 'RGB')
    except Exception as e:
      print(e)
      continue

    #name.append(img_name)
    img = torch.stack([compose(img).to(device)])
    
    
    #print(fear,fe)
    process(fear,fe)
    process(neglect,neg)
    process(irritation,ir)
    process(rage,ra)
    process(disgust,disg)
    process(nervousness,ner)
    process(shame,sh)
    process(disappointment,disa)
    process(envy,en)
    process(suffering,su)
    process(sadness,sa)
    process(joy,jo)
    process(pride,pr)
    sar.append(sarcasm)
    
  
    #txt = torch.as_tensor(txt)
    with torch.no_grad():
      temp_txt = text_model([txt]).detach().cpu().numpy()
      text_features.append(temp_txt)
      temp_img = clip_model.encode_image(img).detach().cpu().numpy()
      image_features.append(temp_img)

      del temp_txt
      del temp_img
      
      torch.cuda.empty_cache()
    
    del img
    #del txt
    torch.cuda.empty_cache()
  return text_features,image_features, fe, neg, ir, ra, disg, ner, sh, disa, en, su, sa, jo, pr, sar

class HatefulDataset(Dataset):

  def __init__(self,data):
    
    self.t_f,self.i_f,self.fe, self.neg, self.ir, self.ra, \
    self.disg, self.ner, self.sh, self.disa, self.en, self.su, self.sa, self.jo, self.pr, \
    self.sar = get_data(data)
    self.t_f = np.squeeze(np.asarray(self.t_f),axis=1)
    self.i_f = np.squeeze(np.asarray(self.i_f),axis=1)

    
    
  def __len__(self):
    return len(self.a)

  def __getitem__(self,idx):
    if torch.is_tensor(idx):
      idx = idx.tolist()
    #print(idx)
    



    
    T = self.t_f[idx,:]
    I = self.i_f[idx,:]
    
    fe = self.fe[idx]
    neg = self.neg[idx]
    ir = self.ir[idx]
    ra = self.ra[idx]
    disg = self.disg[idx]
    ner = self.ner[idx]
    sh = self.sh[idx]
    disa = self.disa[idx]
    en = self.en[idx]
    su = self.su[idx] 
    sa = self.sa[idx]
    jo = self.jo[idx]
    pr = self.pr[idx]
    sar = self.sar[idx]
    
    #name = self.name[idx]

    sample = {'processed_txt':T,'processed_img':I , 'fear': fe, 'neglect': neg, \
              'irritation':ir, 'rage':ra, 'disgust':disg, 'nervousness':ner, 'shame':sh, 'disappointment':disa, \
              'envy':en, 'suffering':su, 'sadness':sa, 'joy':jo, 'pride':pr, 'sarcasm':sar}
    return sample

outliers = []
for names in tqdm(list(data['Name'])):
  if not os.path.exists('/content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/my_meme_data/'+names):
    outliers.append(names)

# outliers

data = data[~data['Name'].isin(outliers)]

len(data)

# dataset = HatefulDataset(data)

class HatefulDatasetFinal(Dataset):

  def __init__(self,data,dataset,outliers):
    
    self.name, self.t_f,self.i_f,self.fe, self.neg, self.ir, self.ra, \
    self.disg, self.ner, self.sh, self.disa, self.en, self.su, self.sa, self.jo, self.pr, \
    self.sar = \
    list(data['Name']), \
    [i['processed_txt'] for i in dataset], \
    [i['processed_img'] for i in dataset], \
    [i['fear'] for i in dataset], \
    [i['neglect'] for i in dataset], \
    [i['irritation'] for i in dataset], \
    [i['rage'] for i in dataset], \
    [i['disgust'] for i in dataset], \
    [i['nervousness'] for i in dataset], \
    [i['shame'] for i in dataset], \
    [i['disappointment'] for i in dataset], \
    [i['envy'] for i in dataset], \
    [i['suffering'] for i in dataset], \
    [i['sadness'] for i in dataset], \
    [i['joy'] for i in dataset], \
    [i['pride'] for i in dataset], \
    [i['sarcasm'] for i in dataset], \
    
    
    self.t_f = np.asarray(self.t_f)
    self.i_f = np.asarray(self.i_f)
   
    
  def __len__(self):
    return len(self.name)

  def __getitem__(self,idx):
    if torch.is_tensor(idx):
      idx = idx.tolist()
    #print(idx)
    


    #print(idx)
    
    T = self.t_f[idx,:]
    I = self.i_f[idx,:]
    
    fe = self.fe[idx]
    neg = self.neg[idx]
    ir = self.ir[idx]
    ra = self.ra[idx]
    disg = self.disg[idx]
    ner = self.ner[idx]
    sh = self.sh[idx]
    disa = self.disa[idx]
    en = self.en[idx]
    su = self.su[idx] 
    sa = self.sa[idx]
    jo = self.jo[idx]
    pr = self.pr[idx]
    sar = self.sar[idx]
   
    
    name = self.name[idx]

    sample = {'name':name, 'processed_txt':T,'processed_img':I , 'fear': fe, 'neglect': neg, \
              'irritation':ir, 'rage':ra, 'disgust':disg, 'nervousness':ner, 'shame':sh, 'disappointment':disa, \
              'envy':en, 'suffering':su, 'sadness':sa, 'joy':jo, 'pride':pr, 'sarcasm':sar}
    return sample

"""
for i in sample_dataset:
  print(i)
"""

#!pip install pytorch-lightning
import pytorch_lightning as pl

import torch
import torch.nn as nn
import torch.nn.functional as F
class fusion(nn.Module):
    def __init__(self,img_feat_size, txt_feat_size, is_first, K, O, DROPOUT_R):
        super(fusion, self).__init__()
        #self.__C = __C
        self.K = K
        self.O = O
        self.DROPOUT_R = DROPOUT_R

        self.is_first = is_first
        self.proj_i = nn.Linear(img_feat_size, K * O)
        self.proj_t = nn.Linear(txt_feat_size, K * O)
        
        self.dropout = nn.Dropout(DROPOUT_R)
        self.pool = nn.AvgPool1d(K, stride = K)

    def forward(self, img_feat, txt_feat, exp_in=1):
        
        batch_size = img_feat.shape[0]
        img_feat = self.proj_i(img_feat)                
        txt_feat = self.proj_t(txt_feat)             
        
        exp_out = img_feat * txt_feat             
        exp_out = self.dropout(exp_out) if self.is_first else self.dropout(exp_out * exp_in)    
        z = self.pool(exp_out) * self.K         
        z = F.normalize(z.view(batch_size, -1))         
        z = z.view(batch_size, -1, self.O)      
        return z

import pickle
#hm_data_hard = HatefulDataset(data)

#torch.save(hm_data_hard,'/content/hm_data_hard_new.pt')

#!cp /content/hm_data_hard_new.pt /content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/

hm_final = torch.load('/content/drive/.shortcut-targets-by-id/1Z57L19m3ZpJ6bEPdyaIMYuI00Tc2RT1I/memes_our_dataset_hindi/hm_data_hard_new.pt')

len(hm_final)

hm_final = HatefulDatasetFinal(data,hm_final,outliers)

import torch

len(hm_final)

"""
hm_final = hm_data_hard
torch.manual_seed(123)
t_p,v_p = torch.utils.data.random_split(hm_final,[90,10])
torch.manual_seed(123)
t_p,te_p = torch.utils.data.random_split(t_p,[80,10])
"""

torch.manual_seed(123)
t_p,te_p = torch.utils.data.random_split(hm_final,[5908,1478])

torch.manual_seed(123)
t_p,v_p = torch.utils.data.random_split(t_p,[5022,886])

# k =0
# for i in hm_final:
#   print(i)
#   k+=1
#   if k==5:
#     break

def get_data_memotion(dataset_path):

  k = pd.read_csv(dataset_path)
  text = list(k['ocr_text'])
  img_path = list(k['name'])
  dataframe = k.apply(LabelEncoder().fit_transform)
  sarcasm = list(dataframe['sarcastic'])
  offensive = list(dataframe['offensive'])
  sentiment = list(dataframe['overall_sentiment'])

  text_features,image_features = [],[]
  for txt,img in tqdm(zip(text,img_path)):
    #txt = clip.tokenize(txt,truncate=True).to(device)
   
    #img = preprocess(Image.open('/content/train_images/'+img)).unsqueeze(0).to(device)
    img = Image.open('/content/train_images/'+img)
    img = torch.stack([compose(img).to(device)])
    with torch.no_grad():
      
      temp_txt = text_model([txt]).detach().cpu().numpy()
      text_features.append(temp_txt)
      temp_img = clip_model.encode_image(img).detach().cpu().numpy()
      image_features.append(temp_img)

      del temp_txt
      del temp_img
      #del temp_c
      torch.cuda.empty_cache()
    del txt
    del img
    #del c
    torch.cuda.empty_cache()

  

  text_features = np.squeeze(np.asarray(text_features,dtype=np.float32),axis=1)
  
  image_features = np.squeeze(np.asarray(image_features,dtype=np.float32),axis=1)
  

  return text_features,image_features, sarcasm, offensive, sentiment

class HatefulDatasetMemotion(Dataset):

  def __init__(self,data_path):
    
    self.t_f,self.i_f,self.sarcasm,self.label,self.sentiment = get_data_memotion(data_path)
    self.t_f = np.asarray(self.t_f)
    self.i_f = np.asarray(self.i_f)
    self.sarcasm = np.asarray(self.sarcasm)
    self.label = np.asarray(self.label)
    self.sentiment = np.asarray(self.sentiment)
    
    
    
    
  def __len__(self):
    return len(list(self.label))

  def __getitem__(self,idx):
    if torch.is_tensor(idx):
      idx = idx.tolist()
    



    label = self.label[idx]
    T = self.t_f[idx,:]
    I = self.i_f[idx,:]
    sarcasm = self.sarcasm[idx]
    sentiment = self.sentiment[idx]
    
    
      
    
    

    




    sample = {'label':label,'processed_txt':T,'processed_img':I,'sarcasm':sarcasm,'sentiment':sentiment}
    return sample

#import torch
#t_m = torch.load('/content/drive/MyDrive/memotion2/memotion_train.pt')
#t_v = torch.load('/content/drive/MyDrive/memotion2/memotion_val.pt')

from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, recall_score,precision_score
import torch
from torch import nn
import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from torch.nn import functional as F
from torchvision.datasets import MNIST
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
import os
import warnings
import torch
#t_m = HatefulDatasetMemotion('/content/train/train_data.csv')

t_m = torch.load('/content/drive/MyDrive/memotion2/memotion_multilingual_train.pt')
v_m = torch.load('/content/drive/MyDrive/memotion2/memotion_multilingual_val.pt')

#torch.manual_seed(123)
#t_m,v_m = torch.utils.data.random_split(t_m,[7000,500])

#torch.save(t_m,'/content/memotion_multilingual_train.pt')
#torch.save(v_m,'/content/memotion_multilingual_val.pt')

#!cp '/content/memotion_multilingual_train.pt' '/content/memotion_multilingual_val.pt'  '/content/drive/MyDrive/memotion2'

# k=0
# for i in t_m:
#   print(i)
#   k+=1
#   if k==5:
#     break

# !pip install pytorch-lightning==1.8.0

#on memotion 2.0

warnings.filterwarnings("ignore", category=DeprecationWarning) 
class ClassifierMemotion(pl.LightningModule):

  def __init__(self):
    super().__init__()

    self.MFB = fusion(640,640,True,256,64,0.1)
    
    self.fin = torch.nn.Linear(64,4)
    self.fin_sarcasm = torch.nn.Linear(64,4)
    self.fin_sentiment = torch.nn.Linear(64,3)
    self.dropout_op = torch.nn.Dropout(0.2)
    
    
    

  def forward(self, x,y):
      
      x_,y_ = x,y
    
      #x = torch.cat((x,nrc),1)
      #print(x,y)
      #z = self.MFB(torch.unsqueeze(y.float(),axis=1),torch.unsqueeze(x.float(),axis=1))
      z = self.MFB(torch.unsqueeze(y.float(),axis=1),torch.unsqueeze(y.float(),axis=1))

      c = self.fin(torch.squeeze(z,dim=1))
      c_sarcasm = self.fin_sarcasm(torch.squeeze(z,dim=1))
      c_sentiment = self.fin_sentiment(torch.squeeze(z,dim=1))
      # probability distribution over labels
      c = torch.log_softmax(c, dim=1)
      c_sarcasm = torch.log_softmax(c_sarcasm, dim=1)
      c_sentiment = torch.log_softmax(c_sentiment, dim=1)
      #c_emo = torch.softmax(c_emo, dim=1)
      return z,c,c_sarcasm,c_sentiment

  def cross_entropy_loss(self, logits, labels):
    return F.nll_loss(logits, labels)

  def training_step(self, train_batch, batch_idx):
      lab,txt,img,sarcasm,sentiment = train_batch
      lab = train_batch[lab]
      txt = train_batch[txt]
      img = train_batch[img]
      sarcasm = train_batch[sarcasm]
      sentiment = train_batch[sentiment]
      
      
      hidden,logits,logit_sarcasm,logit_sentiment = self.forward(txt,img)
      loss1 = self.cross_entropy_loss(logits, lab)
      loss2 = self.cross_entropy_loss(logit_sarcasm, sarcasm)
      loss3 = self.cross_entropy_loss(logit_sentiment, sentiment)
      #loss = loss1+loss2+loss3
      #loss = loss3
      loss = loss2+loss3
      self.log('train_loss', loss)
      return loss


  def validation_step(self, val_batch, batch_idx):
      lab,txt,img,sarcasm,sentiment = val_batch
      lab = val_batch[lab]
      txt = val_batch[txt]
      img = val_batch[img]
      sarcasm = val_batch[sarcasm]
      sentiment = val_batch[sentiment]
      
      
      hidden,logits,logit_sarcasm,logit_sentiment = self.forward(txt,img)
      tmp = np.argmax(logits.detach().cpu().numpy(),axis=-1)
      loss = self.cross_entropy_loss(logits, lab)
      lab = lab.detach().cpu().numpy()
      self.log('val_acc', accuracy_score(lab,tmp))
      self.log('val_acc_sarcasm', f1_score(sarcasm.detach().cpu().numpy(),np.argmax(logit_sarcasm.detach().cpu().numpy(),axis=-1),average='macro'))
      #self.log('val_roc_auc',roc_auc_score(lab,tmp))
      self.log('val_loss', loss)
      tqdm_dict = {'val_acc': accuracy_score(lab,tmp)}
      #print('Val acc {}'.format(accuracy_score(lab,tmp)))
      return {
                'progress_bar': tqdm_dict,
              'val_acc_sarcasm': f1_score(sarcasm.detach().cpu().numpy(),np.argmax(logit_sarcasm.detach().cpu().numpy(),axis=-1),average='macro'),
              'val_acc_sentiment': f1_score(sentiment.detach().cpu().numpy(),np.argmax(logit_sentiment.detach().cpu().numpy(),axis=-1),average='macro')
      }
      
  def validation_epoch_end(self, validation_step_outputs):
    outs = []
    for out in validation_step_outputs:
      outs.append(out['val_acc_sarcasm'])
    self.log('val_acc_all', sum(outs)/len(outs))
    print(f'***Acc at epoch end {sum(outs)/len(outs)}****')

  def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=5e-3)
    return optimizer

  def predict_step(self, batch, batch_idx: int , dataloader_idx: int = None):
      lab,txt,img,sarcasm,sentiment = batch
      lab = batch[lab]
      txt = batch[txt]
      img = batch[img]
      z,_,_,_ = self(txt,img)
      return z
class HmDataModule(pl.LightningDataModule):

  def setup(self, stage):
    
      
    
    self.hm_train = t_m
    self.hm_test = v_m
    

  def train_dataloader(self):
    return DataLoader(self.hm_train, batch_size=128)

  def val_dataloader(self):
    return DataLoader(self.hm_test, batch_size=64)

data_module = HmDataModule()
from pytorch_lightning.callbacks import ModelCheckpoint
checkpoint_callback = ModelCheckpoint(
     monitor='val_acc_all',
     dirpath='primary/ckpts/',
     filename='memotion2-ckpt-epoch{epoch:02d}-val_acc_all{val_acc_all:.2f}',
     auto_insert_metric_name=False,
     save_top_k=1,
    mode="max",
 )
# train
from pytorch_lightning import seed_everything
seed_everything(123, workers=True)
hm_model_memotion = ClassifierMemotion()
#trainer = pl.Trainer(gpus=1,deterministic=True,max_epochs=60,callbacks=[checkpoint_callback])
trainer = pl.Trainer(gpus=1,max_epochs=40,callbacks=[checkpoint_callback])

trainer.fit(hm_model_memotion, data_module)

!ls primary/ckpts

#!rm -rf primary

# !cp /content/primary/ckpts/memotion2-ckpt-epoch16-val_acc_all0.31.ckpt /content/drive/MyDrive/memotion2/ckpts

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# hm_model_memotion = hm_model_memotion.load_from_checkpoint('/content/primary/ckpts/memotion2-ckpt-epoch30-val_acc_all0.29.ckpt')
# hm_model_memotion.to(device)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
hm_model_memotion = hm_model_memotion.load_from_checkpoint('./primary/ckpts/memotion2-ckpt-epoch13-val_acc_all0.29-v1.ckpt')
hm_model_memotion.to(device)

hm_model_memotion.eval()

t,pr = [],[]
for i in v_m:
  _,_,_,z = hm_model_memotion(torch.tensor(i['processed_txt']).to(device).unsqueeze(0), torch.tensor(i['processed_img']).to(device).unsqueeze(0))
  t.append(i['sentiment'])
  pr.append(np.argmax(z.cpu().detach().numpy(),axis=-1)[0])

# pr

from sklearn.metrics import confusion_matrix

confusion_matrix(t,pr)

t_d = DataLoader(te_p, batch_size=64)

# names = []
# sentiment = []
# for i in t_d:
#   print(i['name'])
#   with torch.no_grad():
#     names.extend(i['name'])
#     _,_,_,sent = hm_model_memotion(i['processed_txt'],i['processed_img'])
#     sent = np.argmax(sent.detach().numpy(),axis=-1)
#     sentiment.extend(sent)

# d = {'names': names, 'sentiment': sentiment}

# df = pd.DataFrame.from_dict(d)

# df

# df.to_csv('test_psudo_label_sent.csv')

#!rm -rf /content/our_ds/ckpts

# !rm -rf primary

final_train = {}
final_val = {}

o_p,e1_p,e2_p,e3_p,e4_p,e5_p,e6_p,e7_p,e8_p,e9_p,e10_p,e11_p,e12_p,e13_p,i_p = \
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
o_t,e1_t,e2_t,e3_t,e4_t,e5_t,e6_t,e7_t,e8_t,e9_t,e10_t,e11_t,e12_t,e13_t,i_t = \
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
def append_p(tba,appendee):
  for i in np.argmax(tba.detach().cpu().numpy(),axis=-1):
    appendee.append(i)
def append_gt(tba,appendee):
  for i in tba.detach().cpu().numpy():
    appendee.append(i)
N = []
val_f1,train_f1 = [],[]

# import os
# os.environ['CUBLAS_WORKSPACE_CONFIG']=":16:8"

device

!pip install shutup

# !rm -rf ./noemo

# batch_size=32
class KI(nn.Module):
    def __init__(self):
        super(KI, self).__init__()
        #self.__C = __C
        self.U = torch.nn.Parameter(torch.rand(64, 1, requires_grad=True))
        self.V = torch.nn.Parameter(torch.rand(64, 1, requires_grad=True))
        self.b = torch.nn.Parameter(torch.rand(1, requires_grad=True))

        self.w1 = torch.nn.Parameter(torch.rand(1, requires_grad=True))
        self.w2 = torch.nn.Parameter(torch.rand(1, requires_grad=True))
        self.dropout = nn.Dropout(0.1)
    def forward(self, z, hidden_pred):
        batch_size = z.shape[0]
        importance_weight = torch.nn.Sigmoid()(torch.squeeze(z,dim=1)@self.U + torch.squeeze(hidden_pred,dim=1)@self.V + self.b)

        # print('IW',importance_weight)

        m_t_updated = importance_weight*torch.squeeze(z,dim=1) + (1-importance_weight)*torch.squeeze(hidden_pred.to(device),dim=1)

        m_t_updated_ = self.w1*m_t_updated + self.w2*torch.squeeze(z,dim=1)

        z = torch.unsqueeze(m_t_updated_,axis=1)
        # z = self.dropout(z)

        # z = F.normalize(z.view(batch_size, -1),p=3.0)         # (N, C*O)
        # z = z.view(batch_size, -1, 64) 
        return z

#THIS is for determining perf on our dataset (sarcasm+emotion)
import shutup;shutup.please()
pred_e = 0
import torch
from torch import nn
import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from torch.nn import functional as F
from torchvision.datasets import MNIST
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, recall_score,precision_score
from pytorch_lightning.callbacks import ModelCheckpoint
from sklearn.metrics import roc_auc_score
import os

class Classifier(pl.LightningModule):

  def __init__(self):
    super().__init__()

    self.fusion = fusion(640,640,True,256,64,0.3)
    self.loss_fn_emotion=torch.nn.KLDivLoss(reduction='batchmean',log_target=True)
   
    self.encode_text = torch.nn.Linear(1280,64)
    self.fin = torch.nn.Linear(64,2)
    
    self.fin_sarcasm = torch.nn.Linear(64,3)
    self.fin_e1 = torch.nn.Linear(64,2)
    self.fin_e2 = torch.nn.Linear(64,2)
    self.fin_e3 = torch.nn.Linear(64,2)
    self.fin_e4 = torch.nn.Linear(64,2)
    self.fin_e5 = torch.nn.Linear(64,2)
    self.fin_e6 = torch.nn.Linear(64,2)
    self.fin_e7 = torch.nn.Linear(64,2)
    self.fin_e8 = torch.nn.Linear(64,2)
    self.fin_e9 = torch.nn.Linear(64,2)
    self.fin_e10 = torch.nn.Linear(64,2)
    self.fin_e11 = torch.nn.Linear(64,2)
    self.fin_e12 = torch.nn.Linear(64,2)
    self.fin_e13 = torch.nn.Linear(64,2)
    self.fin_inten = torch.nn.Linear(64,3)
    self.fin_target_ident = torch.nn.Linear(64,7)
    self.fin_emotion_mult = torch.nn.Linear(64,13)

  

    self.KI = KI()

  def forward(self, x,y, hidden_pred):
      
      x_,y_ = x,y
      x = x.float()
      y = y.float()
      
      z_ = self.fusion(torch.unsqueeze(y,axis=1),torch.unsqueeze(x,axis=1))
     

      z = self.KI(z_,hidden_pred)
      # z=z_
    
      
      c_sarcasm = self.fin_sarcasm(torch.squeeze(z,dim=1))
      
      c_sarcasm = torch.log_softmax(c_sarcasm, dim=1)
      
    
      c_emotion = self.fin_emotion_mult(torch.squeeze(z,dim=1))
      return z, c_sarcasm, c_emotion

  def cross_entropy_loss(self, logits, labels):
    return F.nll_loss(logits, labels)
  

  def training_step(self, train_batch, batch_idx):
      _,txt,img,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,sarcasm = train_batch
      
      # lab = train_batch[lab]
      #print(lab)
      txt = train_batch[txt]
      #print(txt)
      
      img = train_batch[img]
     
      e1 = train_batch[e1]
      e2 = train_batch[e2]
      e3 = train_batch[e3]
      e4 = train_batch[e4]
      e5 = train_batch[e5]
      e6 = train_batch[e6]
      e7 = train_batch[e7]
      e8 = train_batch[e8]
      e9 = train_batch[e9]
      e10 = train_batch[e10]
      e11 = train_batch[e11]
      e12 = train_batch[e12]
      e13 = train_batch[e13]
      
      sarcasm = train_batch[sarcasm]
      with torch.no_grad():
        hidden_pred,_,_,_ = hm_model_memotion(txt.to(device),img.to(device))



      

      gt_emotion = torch.cat((torch.unsqueeze(e1,1),torch.unsqueeze(e2,1),torch.unsqueeze(e3,1),torch.unsqueeze(e4,1),torch.unsqueeze(e5,1),torch.unsqueeze(e6,1),\
                              torch.unsqueeze(e7,1),torch.unsqueeze(e8,1),torch.unsqueeze(e9,1),torch.unsqueeze(e10,1),torch.unsqueeze(e11,1),torch.unsqueeze(e12,1),\
                              torch.unsqueeze(e13,1)),1)

      z,logit_sarcasm,logit_emotion = self.forward(txt,img,hidden_pred) # logit_target is logits of target
      
      hidden_pred = torch.squeeze(hidden_pred,dim=1)
      hidden_pred = F.log_softmax(hidden_pred / 1).float()
      z = torch.squeeze(z,dim=1)
      z = F.log_softmax(z / 1).float()
      loss_transfer = self.loss_fn_emotion(z, hidden_pred)
    
      
      
      loss_emo_mult = F.binary_cross_entropy_with_logits(logit_emotion.float(), gt_emotion.float())
      loss_sarcasm = self.cross_entropy_loss(logit_sarcasm, sarcasm)
      
      loss = loss_sarcasm+loss_emo_mult
      # loss = loss_sarcasm
     
      self.log('train_loss', loss)
      f1_sarcasm = f1_score(sarcasm.detach().cpu().numpy(),np.argmax(logit_sarcasm.detach().cpu().numpy(),axis=-1),average='macro')

      #return loss
      return {"loss": loss, "f1": f1_sarcasm}
  def training_epoch_end(self, training_step_outputs):
    out_f1 = []
    for out in training_step_outputs:
      out_f1.append(out['f1'])
    train_f1.append(sum(out_f1)/len(out_f1))
    


  def validation_step(self, val_batch, batch_idx):
      _,txt,img,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,sarcasm = val_batch
      #print(val_batch)
      # lab = val_batch[lab]
      txt = val_batch[txt]
      img = val_batch[img]
      
      e1 = val_batch[e1]
      e2 = val_batch[e2]
      e3 = val_batch[e3]
      e4 = val_batch[e4]
      e5 = val_batch[e5]
      e6 = val_batch[e6]
      e7 = val_batch[e7]
      e8 = val_batch[e8]
      e9 = val_batch[e9]
      e10 = val_batch[e10]
      e11 = val_batch[e11]
      e12 = val_batch[e12]
      e13 = val_batch[e13]
      sarcasm = val_batch[sarcasm]
      
      gt_emotion = torch.cat((torch.unsqueeze(e1,1),torch.unsqueeze(e2,1),torch.unsqueeze(e3,1),torch.unsqueeze(e4,1),torch.unsqueeze(e5,1),torch.unsqueeze(e6,1),\
                              torch.unsqueeze(e7,1),torch.unsqueeze(e8,1),torch.unsqueeze(e9,1),torch.unsqueeze(e10,1),torch.unsqueeze(e11,1),torch.unsqueeze(e12,1),\
                              torch.unsqueeze(e13,1)),1)
      with torch.no_grad():
        hidden_pred,_,_,_ = hm_model_memotion(txt.to(device),img.to(device))
      _,logit_sarcasm,logit_emotion = self.forward(txt,img,hidden_pred)
      


      
      
      
      return {
                
              'val_loss_emotion_multilabel': F.binary_cross_entropy_with_logits(logit_emotion.float(), gt_emotion.float()),
              
       'val_acc sarcasm': accuracy_score(sarcasm.detach().cpu().numpy(),np.argmax(logit_sarcasm.detach().cpu().numpy(),axis=-1)),
       'f1 sarcasm': f1_score(sarcasm.detach().cpu().numpy(),np.argmax(logit_sarcasm.detach().cpu().numpy(),axis=-1),average='macro')
      }
      
  def validation_epoch_end(self, validation_step_outputs):
    outs16,outs17 = [],[]
  
    outs18 = []
    for out in validation_step_outputs:
      
      outs16.append(out['val_loss_emotion_multilabel'])
      outs17.append(out['val_acc sarcasm'])
      outs18.append(out['f1 sarcasm'])
    
    self.log('val_loss_all emo', sum(outs16)/len(outs16))
    self.log('val_acc_all sarcasm', sum(outs17)/len(outs17))
    self.log('val_f1_all sarcasm', sum(outs18)/len(outs18))
    
    # print(f'***f1 at epoch end {sum(outs)/len(outs)}****')
    # print(f'***val acc inten at epoch end {sum(outs14)/len(outs14)}****')
    # print(f'***val loss emotion at epoch end {sum(outs16)/len(outs16)}****')
    print(f'***val acc sarcasm at epoch end {sum(outs17)/len(outs17)}****')
    print(f'***val f1 sarcasm at epoch end {sum(outs18)/len(outs18)}****')
    print('********************')
    val_f1.append(sum(outs18)/len(outs18))

  
  def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=0.001, weight_decay=1e-8)
    return optimizer


class HmDataModule(pl.LightningDataModule):

  def setup(self, stage):
    
      
    
    self.hm_train = t_p
    self.hm_val = v_p
    self.hm_test = te_p
    

  def train_dataloader(self):
    return DataLoader(self.hm_train, batch_size=32)

  def val_dataloader(self):
    return DataLoader(self.hm_test, batch_size=64)

  # def test_dataloader(self):
  #   return DataLoader(self.hm_test, batch_size=128)

data_module = HmDataModule()


checkpoint_callback = ModelCheckpoint(
     monitor='val_f1_all sarcasm',
     dirpath='noemo/ckpts/',
     filename='our-ds-ckpt-epoch{epoch:02d}-val_f1_all sarcasm{val_f1_all sarcasm:.2f}',
     auto_insert_metric_name=False,
     save_top_k=1,
    mode="max",
 )
all_callbacks = []
all_callbacks.append(checkpoint_callback)
"""
for i in range(1,14):
  tmp_checkpoint_callback = ModelCheckpoint(
      monitor='val_acc_all e{}'.format(i),
      dirpath='noemo/ckpts/e{}'.format(i),
      filename='our-ds-ckpt-best-emo-{}'.format(i),
      auto_insert_metric_name=False,
      save_top_k=1,
      mode="max",
  )
  all_callbacks.append(tmp_checkpoint_callback)
"""
# train
from pytorch_lightning import seed_everything
seed_everything(123, workers=True)
hm_model = Classifier()
# print(hm_model.parameters())
# for i in hm_model.parameters():
#   print(i)


hm_model.to(device)
# exit(0)



gpus = 1 if torch.cuda.is_available() else 0
trainer = pl.Trainer(gpus=1,max_epochs=10,callbacks=all_callbacks)


trainer.fit(hm_model, data_module)





