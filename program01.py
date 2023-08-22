def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    # Create a dictionary to initialize initial amounts
    player_balances = {acn1: init_amount,
                       acn2: init_amount,
                       acn3: init_amount}
    
    # Create a dictionary to initialize intermediary balances
    intermediary_balances = {imd_acn1: 0,
                             imd_acn2: 0}
    
    # Create a dictionary to initialize initial debt amounts for intermediaries
    debts = {imd_acn1: {acn1: 0, acn2: 0, acn3: 0},
              imd_acn2: {acn1: 0, acn2: 0, acn3: 0}}
    
    # Create a function to distribute sender's balance to cover debts
    def distribute_money(player_balance, imd_debt1, imd_debt2, imd_balance1, imd_balance2):
        min_to_cover = max(abs(imd_debt1), abs(imd_debt2))

        if min_to_cover != 0:
            
            # If balance is not zero
            if player_balance != 0:
                # If balance is greater or equal to the first debt to cover
                if player_balance >= min_to_cover:
                    if imd_debt1 == 0:
                        imd_debt2 = 0
                        imd_balance2 += min_to_cover
                        player_balance -= min_to_cover
                    elif imd_debt2 == 0:
                        imd_debt1 = 0
                        player_balance -= min_to_cover
                        imd_balance1 += min_to_cover
                    elif imd_debt1 == imd_debt2 and imd_debt1 != 0:
                        if player_balance >= 2 * min_to_cover:
                            imd_debt1 = 0
                            imd_debt2 = 0
                            imd_balance1 += min_to_cover
                            imd_balance2 += min_to_cover
                            player_balance -= 2 * min_to_cover
                        else:
                            to_cover_share = player_balance
                            imd_debt1 += to_cover_share / 2
                            imd_debt2 += to_cover_share / 2
                            imd_balance1 += to_cover_share / 2
                            imd_balance2 += to_cover_share / 2
                            player_balance = 0
                    elif imd_debt1 != imd_debt2 and imd_debt1 != 0 and imd_debt2 != 0:
                        if abs(imd_debt1) > abs(imd_debt2):
                            imd_balance1 += abs(imd_debt1)
                            player_balance -= abs(imd_debt1)
                            imd_debt1 = 0
                            new_min = min(player_balance, abs(imd_debt2))
                            imd_debt2 += new_min
                            imd_balance2 += new_min
                            player_balance -= new_min
                        elif abs(imd_debt1) < abs(imd_debt2):
                            player_balance -= abs(imd_debt2)
                            imd_balance2 += abs(imd_debt2)
                            imd_debt2 = 0
                            new_min = min(player_balance, abs(imd_debt1))
                            imd_debt1 += new_min
                            imd_balance1 += new_min
                            player_balance -= new_min
                # If balance < first debt to cover
                else:
                    if imd_debt1 == 0:
                        imd_debt2 += player_balance
                        imd_balance2 += player_balance
                        player_balance = 0
                    elif imd_debt2 == 0:
                        imd_debt1 += player_balance
                        imd_balance1 += player_balance
                        player_balance = 0
                    elif abs(imd_debt1) == abs(imd_debt2) and imd_debt1 != 0:
                        to_cover_share = player_balance
                        imd_debt1 += to_cover_share / 2
                        imd_debt2 += to_cover_share / 2
                        player_balance -= to_cover_share
                        imd_balance1 += to_cover_share / 2
                        imd_balance2 += to_cover_share / 2
                    elif imd_debt1 != imd_debt2 and imd_debt1 != 0 and imd_debt2 != 0:
                        if abs(imd_debt1) > abs(imd_debt2):
                            imd_debt1 += player_balance
                            imd_balance1 += player_balance
                            player_balance = 0
                            imd_debt2 = imd_debt2
                            imd_balance2 = imd_balance2
                        elif abs(imd_debt1) < abs(imd_debt2):
                            imd_debt2 += player_balance
                            imd_balance2 += player_balance
                            player_balance = 0
                            imd_debt1 = imd_debt1
                            imd_balance1 = imd_balance1
            return player_balance, imd_debt1, imd_debt2, imd_balance1, imd_balance2
        return player_balance, imd_debt1, imd_debt2, imd_balance1, imd_balance2

        

    # Iteration over transactions in the log, each being a list
    for transaction in transact_log:
        (sender, recipient) = transaction[0]
        amount = transaction[1]
        intermediary_account = transaction[2]
        commission = transaction[3]
        
        player_balance = player_balances[sender]
        imd_debt2 = debts[imd_acn2][sender]
        imd_debt1 = debts[imd_acn1][sender]
        
        imd_balance1 = intermediary_balances[imd_acn1]
        imd_balance2 = intermediary_balances[imd_acn2]
        
        commission_amount = amount * (commission / 100)
        
        player_balance, imd_debt1, imd_debt2, imd_balance1, imd_balance2 = distribute_money(player_balances[sender], debts[imd_acn1][sender], debts[imd_acn2][sender], intermediary_balances[imd_acn1], intermediary_balances[imd_acn2])
        
        player_balances[sender] = player_balance
        debts[imd_acn1][sender] = imd_debt1
        debts[imd_acn2][sender] = imd_debt2
        intermediary_balances[imd_acn1] = imd_balance1
        intermediary_balances[imd_acn2] = imd_balance2
        
        # CASE 1: If sender's balance is greater than or equal to (amount + commission_amount)
        if player_balances[sender] >= (amount + commission_amount):
            player_balances[sender] -= (amount + commission_amount)
            player_balances[recipient] += amount
            intermediary_balances[intermediary_account] += commission_amount
            
            player_balance, imd_debt1, imd_debt2, imd_balance1, imd_balance2 = distribute_money(
            player_balances[recipient], debts[imd_acn1][recipient], debts[imd_acn2][recipient],
            intermediary_balances[imd_acn1], intermediary_balances[imd_acn2])

            player_balances[recipient] = player_balance
            debts[imd_acn1][recipient] = imd_debt1
            debts[imd_acn2][recipient] = imd_debt2
            intermediary_balances[imd_acn1] = imd_balance1
            intermediary_balances[imd_acn2] = imd_balance2
        
        # CASE 2: If sender's balance is between commission_amount and amount + commission_amount
        elif (amount + commission_amount) > player_balances[sender] >= commission_amount:
            player_balances[sender] = player_balances[sender] - commission_amount
            intermediary_balances[intermediary_account] = intermediary_balances[intermediary_account] + commission_amount
    
        # CASE 3: If sender's balance is less than commission_amount, all money goes to the intermediary and sender goes into negative debt
        elif player_balances[sender] < commission_amount:
            intermediary_balances[intermediary_account] = intermediary_balances[intermediary_account] + player_balances[sender]
            remaining_debt = player_balances[sender] - commission_amount
            debts[intermediary_account][sender] = debts[intermediary_account][sender] + remaining_debt
            player_balances[sender] = player_balances[sender] - player_balances[sender]
            
    # Creating lists of final player balances
    final_player_balances = [int(player_balances[acn1]), int(player_balances[acn2]), int(player_balances[acn3])]
    # Creating lists of final intermediary earnings
    final_intermediary_earnings = [int(intermediary_balances[imd_acn1]), int(intermediary_balances[imd_acn2])]
    # Creating lists of remaining debts for player accounts to intermediaries
    remaining_debts = [[int(debts[imd_acn1][acn1]), int(debts[imd_acn1][acn2]), int(debts[imd_acn1][acn3])],
        [int(debts[imd_acn2][acn1]), int(debts[imd_acn2][acn2]), int(debts[imd_acn2][acn3])]]
        
    # Returning results as a tuple
    return (final_player_balances, final_intermediary_earnings, remaining_debts)
