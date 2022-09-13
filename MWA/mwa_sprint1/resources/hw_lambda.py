def lambda_handler(event, context):

    name = event['name']
    sport = event['sport']

    statement = f"Name: {name} \nSport: {sport}"

    print(statement)

    res = {"statement": statement}

    return res