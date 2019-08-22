import json
import boto3
import datetime 


def lambda_handler(event, context):

    end_date = datetime.date.today()
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = datetime.date.today() - datetime.timedelta(30)
    start_date = start_date.strftime("%Y-%m-%d")
    
    current_month = datetime.date.today()
    current_month = current_month.strftime("%B")
    subject_name = "AWS Billing for the month of " + current_month

    cost = boto3.client('ce')
    response = cost.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=["UNBLENDED_COST"],
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                },
                {
                    "Type": "DIMENSION",
                    "Key": "LINKED_ACCOUNT"
                }
            ]
            
        )
        
        
    result = response["ResultsByTime"]
    accountlist = []
    servicelist = []
    #print("Start Date : " + start_date)
    #print("End Date : " + end_date)
    for results in result:
        html_text = "<style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}th, td {  padding: 5px;  text-align: left;}</style>"
        html_text = html_text +"<h2>" + subject_name + "</h2>"  + "<br>Start Date : " + start_date + "<br> End Date : " + end_date + "<br><br>"
        html_text = html_text + "<table style='width:100%'> <tr><th>Account Number</th> <th>Amount</th> </tr>"
        for group in results["Groups"]:
            if group["Keys"][1] not in accountlist:
                accountlist.append(group["Keys"][1])
            if group["Keys"][0] not in servicelist:
                servicelist.append(group["Keys"][0])
    cost1 = 0.0
    for x in accountlist:
        html_text = html_text + "<tr> <td>" + str(x) + "</td>"
        for group in results["Groups"]:
            cost = group["Metrics"]["UnblendedCost"]["Amount"]
            #print(group["Keys"][0])
            #print(cost)
            if x == group["Keys"][1]:
                #print(x)
                cost1 = cost1 + float(cost)
                #print("Service cost %f" % (cost1))    
        html_text = html_text +  "<td> %f </tr> </td>" % (cost1)
                
    
    return email(html_text)
    
    #return html_text            

def email(cont):
    
    current_month = datetime.date.today()
    current_month = current_month.strftime("%B")
    subject_name = "AWS Billing for the month of " + current_month
    
    AWS_REGION = "us-east-1"
    client1 = boto3.client('ses',region_name=AWS_REGION)
    response = client1.send_email(
        Source='rajeshnair@integratech.ae',
        Destination={
            'ToAddresses': [
                'rajeshnair@integratech.ae',
            ],
            'CcAddresses': [
                'rajeshnair@integratech.ae',
            ],
            'BccAddresses': [
              'rajeshnair@integratech.ae',
            ]
        },
        Message={
            'Subject': {
                'Data': subject_name,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': 'Integra AWS Billing',
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': cont,
                    'Charset': 'UTF-8'
                }
            }
        }
    )
    return response