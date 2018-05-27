import pandas as pd
import numpy as np
plans=pd.read_csv("Sample_Service_Provider.csv")

plans

plans.columns

plans.fillna("NULL", inplace=True)

def setQuantityreqd(): #Checks if plan gives resources more than user requires

    if (plan_name==0):
        return -1

    else:

        if (plans.loc[plans['Plan_Name']==str(plan_name)].shape[0]==0): #Plan absent in db
            return -1

        else:
            current_plan=plans.loc[plans['Plan_Name']==str(plan_name)]
            is_zero_cost=user_df.columns[(user_df == 0).iloc[0]] #retrieves columns where cost is 0


            current_plan=plans.loc[plans['Plan_Name']==str(plan_name)]

            for l_feature in is_zero_cost:
                if (current_plan[l_feature]>(user_quan_df[l_feature]+0.25*current_plan[l_feature])):
                    is_feature_qty_reqd[l_feature]=user_quan_df[l_feature]

        return is_feature_qty_reqd

def CalculateMaxFeature(user_df): #Calculates most expensive feature from dataframe

    ctr_maximum=0

    for l_feature in (user_df.columns):
        if (user_df[l_feature][0]>ctr_maximum):
            l_maximum=user_df[l_feature][0]
            max_feature=l_feature

    max_feature_quantity=user_quan_df[max_feature][0]

    return max_feature,max_feature_quantity

def FilterPlan(plans,feature,feature_quantity): #Filters plan according to feature_quantity

    filter_plans=plans.loc[plans[feature] > feature_quantity-0.5]
    filter_plans=plans.loc[plans[feature] < (1.25*feature_quantity)]

    if (filter_plans.shape[0]==0):
        return -1

    if (user_quan_df[feature][0]>limits[feature][0]):
        filter_plans1=plans.loc[plans[feature]==-1]
        filter_plans2=pd.concat([filter_plans1, filter_plans])
        return (filter_plans2)

    else:
        return (filter_plans)

def FilterServiceType(plans,service_provider,ctr_filter_against=0): #Filters plans according to service provider

    if (ctr_filter_against==1):
            filtered_plans=plans.loc[plans['Service_Provider']!=service_provider]
            return filtered_plans
    else:
            filtered_plans=plans.loc[plans['Service_Provider']==service_provider]
            return filtered_plans

def CalculateCosts(plan_n): # Calculates cost for plan_n

    ctr_i=0

    while(ctr_i<plans.shape[0]):
        if (plans.iloc[ctr_i]["Plan_Name"]==plan_n):
            break
        ctr_i=ctr_i+1

    cost=plans["Plan_Price"][ctr_i]


    for l_feature in user_quan_df.columns:


        ctr_extra=plans[l_feature][ctr_i]-user_quan_df[l_feature][0]


        if (ctr_extra<0)==True:

            extra_quan=ctr_extra*(-1)

            if (l_feature=='Calls'):
                    cost=cost+extra_quan*plans['Extra_Calls'][ctr_i]



            elif(l_feature=='SMS'):
                        cost=cost+extra_quan*plans['Extra_SMS'][ctr_i]



            elif(l_feature=='Data'):
                        cost=cost+extra_quan*plans['Extra_Data'][ctr_i]



            elif(l_feature=='Roaming_Call'):
                        cost=cost+extra_quan*plans['Extra_Roaming'][ctr_i]


    return cost

def search_dict(cost): #Searches for key where 'cost' is value

    for plan_name, plan_cost in di_name_cost.items():    # for name, cost in list.items():  (for Python 3.x)

        if (plan_cost == cost):

            return plan_name

di_name_cost={}

is_costs=[]

def LeastCostPlan(plan_df):    #Returns the plan_name with least expense and monthly savings if plan used

    ctr_i=0

    total_plans=plan_df.shape[0]

    while (ctr_i<total_plans):

        plan_cost= CalculateCosts(plan_df.iloc[ctr_i]["Plan_Name"])

        plan_name= plan_df.iloc[ctr_i]["Plan_Name"]

        di_name_cost.update({plan_name : plan_cost })

        is_costs.append(plan_cost)

        ctr_i=ctr_i+1

    savings=Total_Cost-min(is_costs)
    perfect_plan=search_dict(min(is_costs))

    return perfect_plan,savings

# TODO: service provider name, VAT, total cost, features quantity used, total additional charge (per feature) incurred are required from bill

Total_Cost= 400
VAT=0
Total_Cost=Total_Cost-VAT
user_d = {'Calls': [100], 'Data': [300], 'SMS': [0], 'Roaming_Call': [30]} #Additional cost from bill
user_quantity= {'Calls': [250], 'Data': [10], 'SMS': [20], 'Roaming_Call': [15] }  #Quantity of features used
limits={'Calls': [1000], 'Data': [5], 'SMS':[2500], 'Roaming_Call':[40] }
user_df = pd.DataFrame(data=user_d)
user_quan_df = pd.DataFrame(data=user_quantity)
plan_name=0
service_provider='Airtel'

max_feature,max_feature_quan=CalculateMaxFeature(user_df)

user_df2=user_df.drop([max_feature],axis=1)

second_max_feature,second_max_feature_quan=CalculateMaxFeature(user_df2)

user_df3=user_df2.drop([second_max_feature],axis=1)
third_max_feature,third_max_feature_quantity=CalculateMaxFeature(user_df3)

plans_filtered_max=FilterPlan(plans,max_feature,max_feature_quan) #Plans filtered only according to most expensive feature

plans_filtered=FilterPlan(plans_filtered_max, second_max_feature, second_max_feature_quan)

if (plans_filtered.shape[0]!=0):
    plans_filtered_onnet=FilterServiceType(plans_filtered, service_provider,0)
    plans_filtered_offnet=FilterServiceType(plans_filtered, service_provider, 1)

is_reqd_quant=setQuantityreqd()

if (is_reqd_quant==-1):
        plan_df=plans_filtered
else:
    for l_feature in is_reqd_quant.column:
        plan_df=FilterPlans(plans_filtered, l_feature, reqd_quant[l_feature])

plan_max,savings=LeastCostPlan(plans_filtered_max)

print(plan_max+ " offers savings of Rs." + str(savings))
print("Annual Savings:" + str(12*savings))

if (plans_filtered.shape[0]==0):
    print("No plans.")

else:

    if (plans_filtered_onnet.shape[0]==0):
        print("No "+service_provider+" plans suitable according to your required usage.")

    else:
        plan_onnet=LeastCostPlan(plans_filtered_onnet)
        print(plan_onnet+ " offers savings of Rs." + str(savings) +" monthly")
        print("Annual Savings:" + str(12*savings))


    if (plans_filtered_offnet.shape[0]==0):
        print("No plans outside "+service_provider)
    else:
        plan_offnet,savings=LeastCostPlan(plans_filtered_offnet)

        print(plan_offnet+ " offers savings of Rs." + str(savings) +" monthly")
        print("Annual Savings: " + str(12*savings))
