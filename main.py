
# coding: utf-8

# In[61]:
'''
@sb6632, @hlp276

'''


import numpy as np
def main():
    cmd_file = "inputFile.txt"
    commandfile(cmd_file)


# In[47]:


def inputfromfile(file_name):
    
    a = ''.join(file_name)
    return np.genfromtxt(a+".txt",dtype=None,delimiter='|',names=True,encoding = 'utf-8')


# In[59]:


import re
import csv
import time
def commandfile(cmd_file):
    command_test_file = open(cmd_file,"r")
    for cmd in command_test_file:
        start_time = time.time()
        strip_cmd = cmd.strip()
        split_cmd_and_name = strip_cmd.split(":=")
        
        name_of_file = split_cmd_and_name[0].strip()
        command = split_cmd_and_name[1]
        final_clean_command=re.sub(r"[^a-z\>\<\=\!\+\*\-\/A-Z0-9]+", ' ', command)
        parameters = final_clean_command.split()
        
        if parameters[0] == "inputfromfile":
            result = inputfromfile(parameters[1:])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")
        
        if parameters[0] == "select":
            result = select(parameters[1],parameters[2:])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")

        if parameters[0] == "project":
            result = project(parameters[1],parameters[2:])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")
            
        if parameters[0] == "avg":
            result = avg(parameters[1],parameters[2:],name_of_file+".txt")
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "sum":
            result = sum(parameters[1],parameters[2:])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "count":
            result = count(parameters[1],parameters[2:])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "sumgroup":
            result = sumgroup(parameters[1],parameters[2:],name_of_file)
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            

        if parameters[0] == "avggroup":
            result = avggroup(parameters[1],parameters[2:],name_of_file) 
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "countgroup":
            result = countgroup(parameters[1],parameters[2:],name_of_file) 
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "join":
            list_operator=['<','<=','==','!=','>=','>']
            if parameters[5] not in list_operator:
                result=join(parameters[3],parameters[6],parameters[4],parameters[7],name_of_file)
            else:
                multiple_con=parameters[3:]
                
                b=''
                for i in range(0,len(multiple_con)):
                    b=b+str(multiple_con[i])+' '
                
                multiple_con=b
                multiple_con=multiple_con.strip()
                multiple_con=multiple_con.split("and")
                
                for i in range(0,(len(multiple_con)-1)):
                    condition_list=multiple_con[i]
                    condition_list= condition_list.split()
                    if i==0:
                        A,B=condition(condition_list[0],condition_list[3],condition_list[1],condition_list[4],condition_list[2])
                    else:
                        A,B=condition(A, B, condition_list[1], condition_list[4], condition_list[2])
                join_list=multiple_con[len(multiple_con)-1]
                join_list= join_list.split()
                result=join(A,B,join_list[1],join_list[4],name_of_file)
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            
        if parameters[0] == "sort":
            if len(parameters)<=4:
                result = sort(parameters[1],parameters[3],None)
            else:
                result = sort(parameters[1],parameters[3],parameters[5])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")
            
        if parameters[0] == "movavg":
            result = movavg(parameters[1],parameters[3],parameters[4])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")
            
        if parameters[0] == "movsum":
            result = movsum(parameters[1],parameters[3],parameters[4])
            end_time = time.time()
            print("Final Compute time for "+parameters[0]+" in Seconds=", end_time-start_time)
            outputtofile(result, name_of_file+".txt")
            
        if parameters[0] == "Btree":
            result = Btree(parameters[1],parameters[2],parameters[3],parameters[4],name_of_file)
        if parameters[0] == "Hash":
            result = Hash(parameters[1],parameters[2],parameters[3],parameters[4],name_of_file)
        if parameters[0] == "concat":
            result = concat(parameters[1],parameters[2])
            outputtofile(result, name_of_file+".txt")



    return name_of_file, command
    


# In[25]:


def select(table,exp):
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    
    for i in range(0, len(exp)):
        if "or" in exp[i]:
            exp[i] = ')|'
        elif "and" in exp[i]:
            exp[i] = "&"
        elif "=" in exp[i]:
            exp[i] = "=="
        elif i==0 or(i>=4 and i%4==0):
            exp[i]= "(table"+"['"+exp[i]+"']"
    final_string = ' '.join(exp)
    final_string=final_string+')'
    
    return table[(eval(final_string))]

        
    


# In[26]:


def project(table,exp):
    
    final_string = ' '.join(exp)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    return table[exp]


# In[27]:


def avg(table,exp,name_of_file):
    final_string = ''.join(exp)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8') 
    result =np.mean(table[final_string])
    with open(name_of_file, mode='w',encoding="utf-8") as outresult:
            
            outresult.write(str(result)) 
    return np.mean(table[final_string])


# In[28]:


def sum(table,exp):
    final_string = ''.join(exp)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')  
    result = np.sum(table[final_string])
    with open(name_of_file, mode='w',encoding="utf-8") as outresult:
            outresult.write(str(result))
    return np.sum(table[final_string])


# In[29]:


def count(table,exp):
    final_string = ''.join(exp)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    result = np.size(table[final_string])
    with open(name_of_file, mode='w',encoding="utf-8") as outresult:
            outresult.write(str(result))
    return np.size(table[final_string])


# In[30]:


def sumgroup(table,exp,name_of_file):
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')  
    if len(exp)<=2:
        final_string = ''.join(exp[1])
        sum_string1 = ''.join(exp[0])        
        a=list(np.unique(table[final_string]))
        dict1={}
        list1 = []
        list1.append(' '.join(exp)) 
        
        for i in range (0,len(a)):
            total=0
            for j in table:
                if j[final_string]==a[i]:
                    total=total+int(j[sum_string1])
            dict1[a[i]]=total
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
            outresult.write(' '.join(exp))
            outresult.write('\n')
            for key, value in dict1.items():
                line = str(key)+" "+str(value)
                outresult.write(line)
                outresult.write('\n')
        outresult.close()
        
    else: 
        aggregate_var=exp[0]
        group_var=exp[1:]
        dict1 = {}

        for i in range(len(table)):
            if(tuple(table[i][group_var])) in dict1:
                dict1[tuple(table[i][group_var])] += int(table[i][aggregate_var])
                
            else:
                dict1[tuple(table[i][group_var])] = int(table[i][aggregate_var])
                
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
            outresult.write(' '.join(exp))
            outresult.write('\n')
            for key, value in dict1.items():
                x = ""
                for i in key:
                    x = x+" "+str(i)
                
                line = str(value)+" "+str(x)
                outresult.write(line)
                outresult.write('\n')
        outresult.close()
    
        
        
    return dict1
    
    


# In[31]:


def avggroup(table,exp,name_of_file):
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    if len(exp)<=2:
        
        final_string = ''.join(exp[1])
        sum_string1 = ''.join(exp[0])
        a=list(np.unique(table[final_string]))
        
        dict1={}
        for i in range (0,len(a)):
            total=0
            c = 0
            for j in table:
                if j[final_string]==a[i]:
                    total=total+int(j[sum_string1])
                    c = c+1
            
            dict1[a[i]]=total/c
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
            outresult.write(' '.join(exp))
            outresult.write('\n')
            for key, value in dict1.items():
                line = str(value)+" "+str(key)
                outresult.write(line)
                outresult.write('\n')
        outresult.close()
        
    else:
        aggregate_var=exp[0]
        group_var=exp[1:]
        dict1 = {}
        for i in range(len(table)):
            if(tuple(table[i][group_var])) in dict1:
                dict1[tuple(table[i][group_var])][0] += int(table[i][aggregate_var])
                dict1[tuple(table[i][group_var])][1] += 1
                
            else:
                dict1[tuple(table[i][group_var])] = [int(table[i][aggregate_var]), 1]
        for key in dict1.keys():
            dict1[key][0] = dict1[key][0]/dict1[key][1]
        
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult_n:
            outresult_n.write(' '.join(exp))
            outresult_n.write('\n')
            for key, value in dict1.items():
                x = ""
                for i in key:
                    x = x+" "+str(i)
                
                line = str(value[0])+" "+str(x)
                outresult_n.write(line)
                outresult_n.write('\n')
        outresult_n.close()


# In[32]:


def countgroup(table,exp,name_of_file):
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    if len(exp)<=2:
        final_string = ''.join(exp[1])
        sum_string1 = ''.join(exp[0])
        a=list(np.unique(table[final_string]))
        
        dict1={}
        for i in range (0,len(a)):
            total=0
            c = 0
            for j in table:
                if j[final_string]==a[i]:
                    total=total+int(j[sum_string1])
                    c = c+1
            
            dict1[a[i]]= c
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
            outresult.write(' '.join(exp))
            outresult.write('\n')
            for key, value in dict1.items():
                line = str(value)+" "+str(key)
                outresult.write(line)
                outresult.write('\n')
        outresult.close()
        
    else:
        aggregate_var=exp[0]
        group_var=exp[1:]
        dict1 = {}
        for i in range(len(table)):
            if(tuple(table[i][group_var])) in dict1:
                dict1[tuple(table[i][group_var])][0] += int(table[i][aggregate_var])
                dict1[tuple(table[i][group_var])][1] += 1
                
            else:
                dict1[tuple(table[i][group_var])] = [int(table[i][aggregate_var]), 1]
        for key in dict1.keys():
            dict1[key][0] = dict1[key][0]/dict1[key][1]
        
        with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult_n:
            outresult_n.write(' '.join(exp))
            outresult_n.write('\n')
            for key, value in dict1.items():
                x = ""
                for i in key:
                    x = x+" "+str(i)
                
                line = str(value[1])+" "+str(x)
                outresult_n.write(line)
                outresult_n.write('\n')
        outresult_n.close()


# In[54]:


def join (table1, table2, col1, col2, name_of_file):
    if type(table1) is not np.ndarray:
        
        table1 = np.genfromtxt(table1+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
        table2 = np.genfromtxt(table2+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
    
    colnames1 = table1[0,:]
    colnames2 = table2[0,:]
    index1 = np.where(colnames1 == col1)
    
    index2 = np.where(colnames2 == col2)
    column1=table1[:,index1]
    column2=table2[:,index2]
    column1 = np.array(column1)
    column2 = np.array(column2)

    dat=column1.shape[0]
    x=[]
    y=[]
    jata=column2.shape[0]


    if dat<jata:

        for i in range(len(column1)):
            for j in  range(len(column2)):
                if column1[i]== column2[j]:
                      
                    x.append(i)
                    y.append(j)
                    
        
        A=table2[y,:]
        B=table1[x,:]
        final=np.concatenate([B,A],axis=1)

    else:
        for i in range(len(column2)):
            for j in range(len(column1)):
                if column2[i]== column1[j]:
                    x.append(i)
                    y.append(j)
                    
                    
        A=table1[y,:]
        B=table2[x,:]
        final=np.concatenate([B,A],axis=1)
    
    with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
        outresult.write(('\t'.join(colnames1)+'\t'+'\t'.join(colnames2)))
        outresult.write('\n')
        write_file = csv.writer(outresult, delimiter='\t')
        write_file.writerows(final)
        outresult.close()
    return final
        


# In[34]:


import operator
ops = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt,
    '=': operator.eq
}

def cmp(arg1, op, arg2):
    operation = ops.get(op)
    return operation(arg1, arg2)


# In[35]:


def condition (table1, table2, col1, col2, condition):
    
    table1 = np.genfromtxt(table1+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
    table2 = np.genfromtxt(table2+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
    
    colnames1 = table1[0,:]
    colnames2 = table2[0,:]
    index1 = np.where(colnames1 == col1)
    index2 = np.where(colnames2 == col2)
    column1=table1[:,index1]
    column2=table2[:,index2]
    column1 = np.array(column1)
    column2 = np.array(column2)
    
    dat=column1.shape[0]
    x=[]
    y=[]
    jata=column2.shape[0]


    if dat<jata:

        for i in range(len(column1)):
            
            for j in  range(len(column2)):
                

                if cmp(column1[i], condition, column2[j]):
                      
                    x.append(i)
                    y.append(j)
                    
                    
        A=table2[y,:]
        B=table1[x,:]
        

    else:
        for i in range(len(column2)):
            for j in range(len(column1)):
                if cmp(column2[i], condition, column1[j]):
                    x.append(i)
                    y.append(j)
                    
                    
        A=table1[y,:]
        B=table2[x,:]
        
        
    return A,B
        


# In[36]:


def sort(table, column1, column2):
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True, encoding = 'utf-8')
    if column2== None:
        a = table[column1].astype(int)
        c = np.where(a)
        c = np.array(c)
        c = c.reshape(len(a),)
        d = np.vstack((a, c)).T
        e = np.lexsort(np.fliplr(d).T)
    else:   
        a = table[column1].astype(int)
        b = table[column2].astype(int)
        c = np.where(a)
        c = np.array(c)
        c = c.reshape(len(a),)
        d = np.vstack((a, b, c)).T
        e = np.lexsort(np.fliplr(d).T)
    return(table[e])


# In[37]:


def movavg(table,column,n):
    n = int(n)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    column = table[column]
    cumsum, mavg = [0], []
    for i, x in enumerate(column, 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= n:
            alpha = n
        
        else:
            alpha = i
        mavg.append(((cumsum[i] - cumsum[i-alpha])/alpha))
    
    listofcolumns= table.tolist()   
    for i in range(len(listofcolumns)):
        listofcolumns[i] = listofcolumns[i] + (mavg[i],)

    a = [('movavg', 'f2')]
    b = table.dtype.descr
    c = b+a
    return np.array(listofcolumns,dtype=c)


# In[38]:


def movsum(table,column,n):
    n = int(n)
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',names=True,encoding = 'utf-8')
    column = table[column]
    listofcolumns = table.tolist()
    cumsum,m_sum = [0],[]
   
    for i, x in enumerate(column, 1):
        cumsum.append(cumsum[i-1] + x)
        if i > n:
            alpha = n
            m_sum.append(cumsum[i] - cumsum[i-alpha])
        else:
            alpha = i
           
            m_sum.append(cumsum[i])
    listofcolumns = table.tolist()
    for i in range(len(listofcolumns)):
        listofcolumns[i] = listofcolumns[i] + (m_sum[i],)
    a = [('movsum', 'f2')]
    b = table.dtype.descr
    c = b+a
    return np.array(listofcolumns,dtype=c)


# In[39]:


from BTrees.IOBTree import BTree
def Btree(table,column,condition,condition_value,name_of_file): 
    start_time = time.time()
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
    condition_value = int(condition_value)
    columns = table[0,:]
    column_index=np.where(columns==column)[0][0]
    values=table[1:,:]
    btree = BTree()
    setofkeys = set(values[:,column_index])
    for key in setofkeys:
        indices = (np.where(cmp(values[:,column_index].astype(int),condition, int(key))))
        btree.insert(int(key),indices)
    result = values[btree.get(int(condition_value))]
    end_time = time.time()
    print("Final Compute time for Btree in Seconds=", end_time-start_time)
    with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
        outresult.write('\t'.join(columns))
        outresult.write('\n')
        write_file = csv.writer(outresult, delimiter='\t')
        write_file.writerows(result)
        outresult.close()
    return values[btree.get(int(condition_value))]


# In[40]:


def Hash(table,column,condition,condition_value,name_of_file):
    start_time = time.time()
    table = np.genfromtxt(table+".txt",dtype=None,delimiter='\t',encoding = 'utf-8')
    condition_value = int(condition_value)
    columns = table[0,:]
    column_index=np.where(columns==column)[0][0]
    values=table[1:,:]
    hashtree = dict()
    setofkeys = set(values[:,column_index])
    for keys in setofkeys:
        indices = (np.where(cmp(values[:,column_index].astype(int),condition, int(keys))))
        hashtree[keys]=indices
    result=values[hashtree.get(str(condition_value),condition_value)]
    end_time = time.time()
    print("Final Compute time for Hash in Seconds=", end_time-start_time)
    with open(name_of_file+".txt", mode='w',encoding="utf-8") as outresult:
        outresult.write('\t'.join(columns))
        outresult.write('\n')
        write_file = csv.writer(outresult, delimiter='\t')
        write_file.writerows(result)
        outresult.close()
  
    return values[hashtree.get(str(condition_value),condition_value)]


# In[41]:


def concat(table1,table2):
    table1 = np.genfromtxt(table1+".txt",dtype=None,names=True,delimiter='\t',encoding = 'utf-8')
    table2 = np.genfromtxt(table2+".txt",dtype=None,names=True,delimiter='\t',encoding = 'utf-8')
    
    if table1.size != 1 and table2.size != 1:
        table3 = np.concatenate((table1, table2), axis=0)
    elif table1.size != 1:
        table3 = np.append(table1, table2)
    elif table2.size != 1:
        table3 = np.append(table2, table1)
    else:
        table3 = np.array([table1.dtype.names,table1, table2])
    
    return table3


# In[48]:


def outputtofile(result, name_of_file): 
    with open(name_of_file, mode='w',encoding="utf-8") as outresult:
        write_file = csv.writer(outresult, delimiter='\t')
        write_file.writerow(result.dtype.names)
        write_file = csv.writer(outresult, delimiter='\t')
        write_file.writerows(result)
        outresult.close()


# In[ ]:


main()

