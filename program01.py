
def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    # creo dizionario per inizializzare l'importo iniziale
    saldi_giocatori = {acn1: init_amount, 
                       acn2: init_amount, 
                       acn3: init_amount}
    
    # creo dizionario per inizializzare i saldi degli intermediari
    saldi_intermediari = {imd_acn1: 0, 
                          imd_acn2: 0}
    
    # creo dizionario per inizializzare l'importo iniziale dei debiti nei confornti degli intermediair
    debiti = {imd_acn1: {acn1: 0, acn2: 0, acn3: 0}, 
              imd_acn2: {acn1: 0, acn2: 0, acn3: 0}}
    
    #creo una fuzione che mi distribuisca i soldi del saldo del mittente per ricoprire i debiti
    def distribuisci_soldi(saldo_giocatore, debito_imdacn1,debito_imdacn2,saldo_intermediario1,saldo_intermediario2):
        mini_da_coprire=max(abs(debito_imdacn1),abs(debito_imdacn2))

        if mini_da_coprire !=0:
            
            #seil saldo è diverso da zero
            if saldo_giocatore !=0:
            #se il saldo è maggiore o uguale del primo debito che inizio a coprire
                if saldo_giocatore>=mini_da_coprire:
                #se il debito 1 è uguale a zero e quindi inizio a coprire l'altro
                    if debito_imdacn1 == 0:
                        debito_imdacn2 = 0
                        
                        saldo_intermediario2 += mini_da_coprire
                        saldo_giocatore -=mini_da_coprire
                #se il debito 2 è uguale a zero e quindi inizio a coprire l'altro
                    elif debito_imdacn2==0:
                        debito_imdacn1 = 0
                        saldo_giocatore -=mini_da_coprire

                        saldo_intermediario1 +=mini_da_coprire
                   
                    elif debito_imdacn1 == debito_imdacn2 and debito_imdacn1 != 0 :
                        #Entrambi i debiti sono uguali, copri entrambi in modo equo
                        if saldo_giocatore>=2*(mini_da_coprire):
                             
                            debito_imdacn1 = 0
                            debito_imdacn2 =0
                            
                            saldo_intermediario1 += mini_da_coprire
                            saldo_intermediario2 += mini_da_coprire
                            saldo_giocatore -= (mini_da_coprire * 2)
                        else:
                            quota_da_coprire = saldo_giocatore
                            debito_imdacn1 += (quota_da_coprire/2)
                            debito_imdacn2 += quota_da_coprire/2
                            saldo_intermediario1 += quota_da_coprire/2
                            saldo_intermediario2 += quota_da_coprire/2
                            saldo_giocatore =0
                    elif debito_imdacn1 != debito_imdacn2 and debito_imdacn1 != 0 and debito_imdacn2 != 0:
                        if abs(debito_imdacn1)>abs(debito_imdacn2):
                    
                            saldo_intermediario1 += abs(debito_imdacn1)
                            saldo_giocatore -=  abs(debito_imdacn1)
                            debito_imdacn1=0
                            nuovo_min=min(saldo_giocatore,abs(debito_imdacn2))

                            debito_imdacn2+=nuovo_min
                            saldo_intermediario2 += nuovo_min
                            saldo_giocatore -=nuovo_min
                            
                        elif abs(debito_imdacn1)<abs(debito_imdacn2):
                            saldo_giocatore-=abs(debito_imdacn2)
                            saldo_intermediario2 += abs(debito_imdacn2)
                            debito_imdacn2=0
                            nuovo_min=min(saldo_giocatore,abs(debito_imdacn1))

                            debito_imdacn1 +=nuovo_min
                            saldo_intermediario1 += nuovo_min
                            saldo_giocatore -=nuovo_min
                            
                # se saldo< primo debito da coprire
                else:
                    
                    if debito_imdacn1 == 0:
                        debito_imdacn2 +=saldo_giocatore
                        
                        saldo_intermediario2 += saldo_giocatore
                        saldo_giocatore=0
                #se il debito 2 è uguale a zero e quindi inizio a coprire l'altro
                    elif debito_imdacn2==0:
                        debito_imdacn1 +=saldo_giocatore
                        
                        saldo_intermediario1 += saldo_giocatore
                        saldo_giocatore =0
                   
                    elif abs(debito_imdacn1 )== abs(debito_imdacn2) and debito_imdacn1 != 0 :
                        quota_da_coprire = saldo_giocatore
                        debito_imdacn1 += (quota_da_coprire/2)
                        debito_imdacn2 += (quota_da_coprire/2)
                        saldo_giocatore -= quota_da_coprire
                        saldo_intermediario1 += (quota_da_coprire/2)
                        saldo_intermediario2 += (quota_da_coprire/2)
                    elif debito_imdacn1 != debito_imdacn2 and debito_imdacn1 != 0 and debito_imdacn2 != 0:
                        if abs(debito_imdacn1)>abs(debito_imdacn2):
                            debito_imdacn1+=saldo_giocatore
                            saldo_intermediario1 += saldo_giocatore
                            saldo_giocatore =0
                            debito_imdacn2=debito_imdacn2
                            saldo_intermediario2=saldo_intermediario2
                            
                        
                        elif abs(debito_imdacn1)<abs(debito_imdacn2):
                            debito_imdacn2+=saldo_giocatore
                            saldo_intermediario2 += saldo_giocatore
                            saldo_giocatore =0
                            debito_imdacn1=debito_imdacn1
                            saldo_intermediario1=saldo_intermediario1
                    return saldo_giocatore, debito_imdacn1, debito_imdacn2, saldo_intermediario1, saldo_intermediario2
  
# se entrambi i debiti sono uguali a zero ritorna senza modificare

            return saldo_giocatore, debito_imdacn1, debito_imdacn2,saldo_intermediario1,saldo_intermediario2               
        return saldo_giocatore, debito_imdacn1, debito_imdacn2,saldo_intermediario1,saldo_intermediario2               

    # Iterazione sulle transazioni nel registro che sonoa loro volta liste
    #for transazione in transact_log:
    for transazione in transact_log:
        (mittente, destinatario) = transazione[0]
        importo = transazione[1]
        conto_intermediario = transazione[2]
        commissione = transazione[3]
        
        saldo_giocatore = saldi_giocatori[mittente]
        debito_imdacn2 = debiti[imd_acn2][mittente]
        debito_imdacn1 = debiti[imd_acn1][mittente]
        
        saldo_intermediario1 = saldi_intermediari[imd_acn1]
        saldo_intermediario2 = saldi_intermediari[imd_acn2]
    
        importo_commissione=(importo*(commissione/100))
        
        saldo_giocatore, debito_imdacn1, debito_imdacn2, saldo_intermediario1, saldo_intermediario2 = distribuisci_soldi(saldi_giocatori[mittente], debiti[imd_acn1][mittente], debiti[imd_acn2][mittente],saldi_intermediari[imd_acn1], saldi_intermediari[imd_acn2])
        
        saldi_giocatori[mittente] = saldo_giocatore
        debiti[imd_acn1][mittente] = debito_imdacn1
        debiti[imd_acn2][mittente] = debito_imdacn2
        saldi_intermediari[imd_acn1] = saldo_intermediario1
        saldi_intermediari[imd_acn2] = saldo_intermediario2
        #CASO 1: se  il saldo del giocatore è maggiore o uguale di (importo+importo_commissione)
        if saldi_giocatori[mittente] >= (importo + importo_commissione):
            saldi_giocatori[mittente] -= (importo + importo_commissione)
            saldi_giocatori[destinatario] += importo
            saldi_intermediari[conto_intermediario] += importo_commissione
            
            saldo_giocatore, debito_imdacn1, debito_imdacn2, saldo_intermediario1, saldo_intermediario2 = distribuisci_soldi(
            saldi_giocatori[destinatario], debiti[imd_acn1][destinatario], debiti[imd_acn2][destinatario],
            saldi_intermediari[imd_acn1], saldi_intermediari[imd_acn2])

            saldi_giocatori[destinatario] = saldo_giocatore
            debiti[imd_acn1][destinatario] = debito_imdacn1
            debiti[imd_acn2][destinatario] = debito_imdacn2
            saldi_intermediari[imd_acn1] = saldo_intermediario1
            saldi_intermediari[imd_acn2] = saldo_intermediario
                
      
        #CASO 2: se il saldo del giocatore è compreso tra importo_commmissione  e importo+importo_commissione
        #in questo caso al destinatario non arriva nulla e arriva solo all'intermediario
        
        elif (importo + importo_commissione)>saldi_giocatori[mittente]>= importo_commissione:
            saldi_giocatori[mittente]=saldi_giocatori[mittente]-importo_commissione
            
            saldi_intermediari[conto_intermediario]=saldi_intermediari[conto_intermediario]+ importo_commissione
            
    
        #CASO 3 : se il saldo del giocatore è minore di importo_commissione arrivano tutti i soldi all'intermediario e giocatore rimane in debito negativo
        #in questo caso gestisco i debiti

        elif saldi_giocatori[mittente]<importo_commissione :
            saldi_intermediari[conto_intermediario]=saldi_intermediari[conto_intermediario]+saldi_giocatori[mittente]
            debito_rimanente = saldi_giocatori[mittente] - importo_commissione
            debiti[conto_intermediario][mittente]=debiti[conto_intermediario][mittente] + debito_rimanente
            saldi_giocatori[mittente]-= saldi_giocatori[mittente]
            
                
    # Creazione delle liste di saldo finale dei giocatori
    saldi_finali_giocatori = [int(saldi_giocatori[acn1]),int(saldi_giocatori[acn2]), int(saldi_giocatori[acn3])]
    # Creazione delle liste di importo finale guadagnato dagli intermediari
    importi_finali_intermediari = [int(saldi_intermediari[imd_acn1]), int(saldi_intermediari[imd_acn2])]
    # Creazione delle liste di debiti residui dei conti del giocatore per gli intermediari
    debiti_residui = [[int(debiti[imd_acn1][acn1]), int(debiti[imd_acn1][acn2]), int(debiti[imd_acn1][acn3])],
        [int(debiti[imd_acn2][acn1]), int(debiti[imd_acn2][acn2]), int(debiti[imd_acn2][acn3])]]
        
    
    
  
    # Restituzione dei risultati come tupla
    return (saldi_finali_giocatori, importi_finali_intermediari, debiti_residui)   
