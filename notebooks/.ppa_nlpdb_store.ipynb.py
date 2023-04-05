#!/usr/bin/env python
# coding: utf-8

# ## DB funcs for nlp

# In[2]:


get_ipython().run_line_magic('run', 'ppa_init.ipynb')
get_ipython().run_line_magic('run', 'ppa_nlpfuncs.ipynb')
work=random.choice(digiworks)
work.title, work.pub_date


# ### SQL-style: TotalCount and WordCount

# In[3]:


def store_counts(self, countd=None, **opts):
    if not countd: countd = self.calc_counts()
    total = sum(countd.values())
    
    with timer('init workcount'):
        totalcount, totalcount_created = TotalCount.objects.get_or_create(
            work=self, count=total
        )

    ## store words
    with timer('gathering objects to store'):
        objs = [
            WordCount(
                work=self,
                word=word,
                count=countd[word]
            )
            for word in countd
            if word and countd[word]
        ]

    with timer('bulk storing'):
        res = WordCount.objects.bulk_create(objs, ignore_conflicts=True, batch_size=500)
    
    return res

DigitizedWork.store_counts = store_counts


# In[4]:


objs = work.store_counts()
len(objs), objs[0], objs[0].__dict__


# In[5]:


work.totalcount_set.first().__dict__


# In[6]:


# wwc.work.work


# In[7]:


qset=WordCount.objects.filter(word='ballad')
qset


# ### Storing all counts

# In[8]:


if 1: 
    timer.PRINT = False

    pmap_run(
        store_counts,
        digiworks,
        num_proc=8
    )


# In[ ]:




