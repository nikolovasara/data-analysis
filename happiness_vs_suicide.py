#!/usr/bin/env python
# coding: utf-8

# # (Не)поврзаноста на бројот на самоубиства со „среќните“ земји

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ## 1. Вчитување на податочните множества

# > Податочно множество: Извештај за среќата во светот во 2015 година

# In[2]:


happiness_data=pd.read_csv('2015.csv')


# > Податочно множество: Извештај за самоубиства во светот во 2015 година

# In[3]:


suicides_data=pd.read_csv('who_suicide_statistics.csv')


# ###  Преглед на податоците

# In[4]:


happiness_data.head() # првите 5 реда од податоците


# In[5]:


suicides_data.head()


# #### Број на редови и колони во податочните множества за среќа и самоубиство, соодветно

# In[6]:


print('Number of rows: ',happiness_data.shape[0],'\nNumber of columns: ',happiness_data.shape[1])


# In[7]:


print('Number of rows: ',suicides_data.shape[0],'\nNumber of columns: ',suicides_data.shape[1])


# #### Преглед на содржината на колоните во двете множества

# In[8]:


suicides_data.columns


# In[9]:


happiness_data.columns


# #### Преименување на колоната по која ќе се спојуваат двете множества

# In[10]:


happiness_data = happiness_data.rename(columns={'Country': 'country'})


# ###  Спојување на податочните множества според колоната "country"
# 

# In[11]:


merged_data=pd.merge(happiness_data, suicides_data, on='country')


# ### Анализа на податоците во резултантното множество

# In[12]:


merged_data.head()


# In[13]:


merged_data.columns


# In[14]:


merged_data.shape[0] # број на редови


# In[15]:


merged_data.head()


# In[16]:


merged_data.head()


# ## 2. Прочистување на податоците
# 
# Во резултантното множество има податоци и од други години. Тоа се податоци кои доаѓаат од множеството за самоубиства во светот. Податочното множество за среќата во светот не содржи податоци за други години, освен за 2015 година. Поради тоа, се селектираат податоците кои се само од 2015 година.

# In[17]:


data_2015=merged_data[merged_data['year']==2015]


# In[18]:


data_2015.head()


# Податоците се експортираат за полесен преглед користејќи програма за табеларен преглед на податоци.

# In[19]:


data_2015.to_csv('data_2015.csv')


# In[20]:


data_2015.columns


# Анализирајќи ги податоците, се донесе заклучок дека колоните "Region" и "Standard error" не се потребни за ова истражување и поради тоа се отстрануваат.

# In[21]:


data_2015.drop(columns=['Region','Standard Error',],inplace=True)


# In[22]:


data_2015.columns


# In[23]:


data_2015.shape[0]


# In[24]:


# се отстрануваат сите редови кои содржат null вредности 
data_2015 = data_2015.dropna() 
data_2015.shape[0]


# In[25]:


data_2015['Happiness Rank'].min()


# ## 3. Испитување на податоците
# 
#  - **Број на самоубиства во светот според години и пол**: од графикот долу се гледа дека бројот на самоубиства е поголем кај машкиот пол во скоро сите држави во светот.

# In[26]:


worldwide=sns.lineplot(x='age',y='suicides_no',hue='sex',data=data_2015)


# In[27]:


suicides_by_age=data_2015[data_2015['Happiness Rank']==data_2015['Happiness Rank'].min()][['country','sex','suicides_no','age']].groupby('age')['suicides_no'].sum()


# In[28]:


suicides_by_gender=data_2015[data_2015['Happiness Rank']==data_2015['Happiness Rank'].min()][['country','sex','suicides_no','age']].groupby('sex')['suicides_no'].sum()


# Подетален преглед на распределбата на бројот на самоубиства по возраст и пол

# In[29]:


suicides_by_age


# In[30]:


suicides_by_gender


# „Најсреќна“ земја во светот е онаа земја која има најмала вредност за 'Happiness Rank', односно земјата која има највисок ранг на среќа. Во овој случај тоа е Швајцарија.

# In[31]:


happiest_country=data_2015[data_2015['Happiness Rank']==data_2015['Happiness Rank'].min()][['country','sex','suicides_no','age','population']]
happiest_country


# In[32]:


import matplotlib.pyplot as plt


# In[33]:


fig=plt.figure(figsize=(12,8), dpi= 100, facecolor='w', edgecolor='k')


# In[34]:


plt.rcParams['figure.figsize'] = [10, 5]


# Се додава колона за процент на самоубиства со цел споредбите кои се прават да бидат валидни. Ако се земе само бројот на самоубиства, а не и вкупната популација на која се однесува тој број, тогаш распределбата на бројот на самоубиства во една земја по возраст и пол нема да е релевантна.

# In[35]:


happiest_country['suicides percentage'] = (happiest_country['suicides_no'] / happiest_country['population'])*100


#  - На графикот подолу е прикажана распределбата на самоубиства по пол и возраст во најсреќната земја - Швајцарија.

# In[36]:


ax=sns.lineplot(x='age',y='suicides percentage',hue='sex',data=happiest_country)


# Со иста постапка се анализира и бројот на самоубиства во најнесреќната земја - Египет.

# In[37]:


data_2015[data_2015['Happiness Rank']==data_2015['Happiness Rank'].max()]['country'].unique()[0]


# In[38]:


saddest_country=data_2015[data_2015['Happiness Rank']==data_2015['Happiness Rank'].max()][['country','sex','suicides_no','age','population']]


# In[39]:


saddest_country


# In[40]:


sns.lineplot(x='age',y='suicides_no',hue='sex',data=saddest_country)


# In[41]:


saddest_country['suicides percentage'] = (saddest_country['suicides_no'] / saddest_country['population'])*100


#  - На графикот подолу е прикажана распределбата на самоубиства по пол и возраст во најнесреќната земја - Египет.

# In[42]:


sns.lineplot(x='age',y='suicides percentage',hue='sex',data=saddest_country)


# Со следните два исказа се наоѓаат државите кои имаат најголем и најмал број на самоубиства соодветно, не земајќи ја во предвид вкупната популација.

# In[43]:


suicides_by_country=data_2015.groupby(['country'])['suicides_no'].agg(suicides='sum').query('suicides == suicides.max()')
print(suicides_by_country)


# In[44]:


suicides_by_country_min=data_2015.groupby(['country'])['suicides_no'].agg(suicides='sum').query('suicides == suicides.min()')
print(suicides_by_country_min)


# In[45]:


suicides_country=data_2015.groupby(['country'])['suicides_no'].agg(suicides='sum')


# In[46]:


population_country=data_2015.groupby(['country'])['population'].agg(population='sum')


# In[47]:


suicides_country


# In[48]:


population_country


# Откако се генерираат табелите држава - самоубиства и држава - популација, се спојуваат според државата и се добива резултантата табела подолу. Потоа се додава и нова колона процентот на самоубиства (самоубиства / популација).

# In[49]:


population_suicides=pd.merge(population_country, suicides_country, on='country')
print(population_suicides)


# In[50]:


population_suicides['suicides_percentage'] = (population_suicides['suicides'] / population_suicides['population'])*100


# In[51]:


population_suicides


# Претходно, беа пронајдени земјите со најголем и најмал број на самоубиства не земајќи го во предвид вкупното население. Сега се наоѓаат земјите кои имаат процентуално најмал и процентуално најголем број на самоубиства. Тоа се Египет и Литванија соодветно.

# In[52]:


suicides_percentage_by_country_min=population_suicides.query('suicides_percentage == suicides_percentage.min()')
print(suicides_percentage_by_country_min)


# In[53]:


suicides_percentage_by_country_max=population_suicides.query('suicides_percentage == suicides_percentage.max()')
print(suicides_percentage_by_country_max)


# In[54]:


happinessmetrics_suicides=data_2015.groupby(['country','Economy (GDP per Capita)','Family','Health (Life Expectancy)','Generosity','Dystopia Residual','Trust (Government Corruption)','Freedom']).sum()[['population','suicides_no']]
happinessmetrics_suicides['suicides_percentage'] = (happinessmetrics_suicides['suicides_no'] / happinessmetrics_suicides['population'])*100
happinessmetrics_suicides


# Следно што е анализирано во ова истражување е процентот на самоубиства во државите, зависно од 6 фактори кои се земени при истражувањето за среќата во светот: економија, семејство, здравство, дарежливост, доверба во власта и слобода.

#  - Процент на самоубиства во државите според економијата.

# In[55]:


sns.relplot(x='Economy (GDP per Capita)',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


#  - Процент на самоубиства во државите според фактор семејство.

# In[56]:


sns.relplot(x='Family',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


#  - Процент на самоубиства во државите според здравство.

# In[57]:


sns.relplot(x='Health (Life Expectancy)',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


#  - Процент на самоубиства во државите според дарежливост.

# In[58]:


sns.relplot(x='Generosity',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


# In[59]:


sns.relplot(x='Dystopia Residual',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


#  - Процент на самоубиства во државите според довербата во власта.

# In[60]:


sns.relplot(x='Trust (Government Corruption)',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


#  - Процент на самоубиства во државите според слободата.

# In[61]:


sns.relplot(x='Freedom',y='suicides_percentage',hue='country',data=happinessmetrics_suicides)


# **Причината за самоубиствата не може да се идентифицира лесно. Секоја земја има различни резултати за метриките што носи и многу различни причини и комбинации кои водат до самоубиства.**

# Следната табела и следниот график даваат детален преглед на државите и процентот на самоубиства во секоја држава според полот.

# In[62]:


gender_country_suicides=data_2015.groupby(['country','sex']).sum()[['population','suicides_no']]
gender_country_suicides['suicides_percentage'] = (gender_country_suicides['suicides_no'] / gender_country_suicides['population'])*100
gender_country_suicides


# In[63]:


sns.lineplot(x='country',y='suicides_percentage',hue='sex',data=gender_country_suicides)


# **Може да се заклучи дека машката популација има значително повисок степен на самоубиства од женската популација.**

# In[ ]:




