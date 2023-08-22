# -*- coding: utf-8 -*-

'''
Un sistema di e-cash consente agli utenti registrati di effettuare
    transazioni in valuta elettronica. Indicheremo la moneta elettronica in
    questione con il simbolo Ħ.
    Per il trasferimento di Ħ, gli utenti ricorrono ad agenti intermediari
    che gestiscono le transazioni al prezzo di una commissione. Le
    commissioni di transazione si basano su percentuali variabili, decise
    dagli intermediari.

Lo scopo di questo programma è quello di elaborare un registro delle transazioni
    tra gli utenti del sistema di e-cash che riporti:
    1) una lista con il saldo finale di ogni conto dei giocatori coinvolti;
    2) una lista con l'importo finale guadagnato da ogni intermediario;
    3) una lista in cui, per ogni intermediario, una lista annidata riporta i
       debiti residui dei conti del giocatore (0 se non è stato accumulato
       alcun debito, altrimenti un numero intero negativo).
    I risultati (1), (2) e (3) devono essere elementi di una tupla.

In particolare, deve essere progettata la seguente funzione:
     ex1 (acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
     dove
     - acn1, acn2 e acn3 sono i numeri di conto del giocatore 1, 2 e 3,
       rispettivamente;
     - imd_acn1 e imd_acn2 sono i numeri di conto degli intermediari 1 e 2,
       rispettivamente;
     - init_amount è l'importo iniziale nei conti dei tre giocatori
       (assumiamo che tutti i giocatori inizino con lo stesso importo iniziale);
     - i conti degli intermediari iniziano con un saldo di 0Ħ;
     - transact_log è un elenco di transazioni; ogni transazione è una tupla
       che consta dei seguenti elementi:
       · una coppia di numeri interi indicanti il numero del conto del
         mittente e il numero del conto del destinatario;
       · l'importo trasferito;
       · il numero del conto dell'intermediario;
       · la percentuale della commissione di transazione (da calcolare in
         base all'importo trasferito).

Ad esempio, la seguente tupla:
       ((0x44AE, 0x5B23), 800, 0x1612, 4)
     indica una transazione che trasferisce 800Ħ dal numero di conto 0x44AE al
     conto numero 0x5B23, con il servizio dell'intermediario che riceverà il
     4% di 800Ħ (quindi, 32Ħ) sul proprio conto a 0x1612.
     Di conseguenza,
     - il saldo del mittente (0x44AE) diminuirà di
         800 + 32 = 832Ħ,
     - il saldo del destinatario (0x5B23) aumenterà di
         800Ħ,
     - l'intermediario guadagnerà e depositerà sul proprio conto (0x1612)
         32Ħ.

Si noti che se i fondi nel conto del mittente sono insufficienti,
    la transazione viene dichiarata non valida dall'intermediario.
    L'intermediario riceverà comunque la commissione dal mittente, se ci sono
    abbastanza Ħ nel conto del mittente. Se il mittente non può pagare la
    commissione di transazione, l'intermediario riceverà tutti i fondi
    rimanenti e prenderà la sua parte dalle successive transazioni inviate al
    debitore fino al pagamento del debito. Considerando l'esempio precedente,
    se ci sono solo 700Ħ nel conto 0x44AE, l'intermediario guadagna 32Ħ e
    l'importo in 0x44AE diminuisce a 668Ħ. Se ci sono solo 10Ħ nel conto
    0x44AE, l'intermediario guadagna 10Ħ e l'importo in 0x44AE diminuisce a
    0Ħ; inoltre, l'intermediario mantiene un credito di 22Ħ con il mittente. Il
    mittente sarà obbligato a rimborsare i 22Ħ ottenendo l'importo dovuto
    dalle transazioni ricevute successivamente fino all'estinzione del debito.

    Se si accumula un debito nei confronti di due intermediari, i fondi vanno
    per primo all'intermediario che ha il credito più elevato e il resto va
    all'altro intermediario. Ad esempio, se il giocatore 1 deve 300Ħ
    all'intermediario 1 e 200Ħ all'intermediario 2, quando il giocatore 1
    riceve 400Ħ, 300Ħ vengono pagati all'intermediario 1 e 100Ħ vengono
    pagati all'intermediario 2. Se lo stesso importo è dovuto a entrambi gli
    intermediari, il rimborso è equamente diviso. Ad esempio, il giocatore 2
    deve 100Ħ all'intermediario 1 e 100Ħ all'intermediario 2; quando il
    giocatore 2 riceve 100Ħ, 50Ħ vanno a ciascun intermediario.

Ad esempio,
    ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,
        [ ((0x44AE, 0x5B23),  800, 0x1612,  4),
          ((0x44AE, 0xC78D),  800, 0x90FF, 10),
          ((0xC78D, 0x5B23),  400, 0x1612,  8),
          ((0x44AE, 0xC78D), 1800, 0x90FF, 12),
          ((0x5B23, 0x44AE),  100, 0x1612,  2)
        ]
    ritorna
    ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 100,
        [ ((0x5B23,0xC78D ),  90, 0x1612,  10),
          ((0x5B23, 0xC78D),  100, 0x1612, 10)]
    
    ( [2098, 568, 0], [66, 268], [ [0, 0, 0], [0, 0, -28] ] )
    perché tutti gli utenti iniziano con 1000Ħ nei loro conti ed, al termine,
    – il saldo dell’utente 1 ammonta a 2098Ħ,
    – il saldo dell’utente 2 ammonta a 568Ħ,
    – il saldo dell’utente 3 ammonta a 0Ħ,
    – l'intermediario 1 ha guadagnato 66Ħ,
    – l'intermediario 2 ha guadagnato 268Ħ,
    – l’utente 3 rimane in debito di 28Ħ con l'intermediario 2.

Il TIMEOUT per ciascun test è di 0.5 secondi

ATTENZIONE: è proibito:
    - importare altre librerie
    - usare variabili globali
    - aprire file
'''
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
            saldi_intermediari[imd_acn2] = saldo_intermediario2
            
            
            
            
            
      
                
      
        #CASO 2: se il saldo del giocatore è compreso tra importo_commmissione  e importo+importo_commissione
        #in questo caso al destinatario non arriva nulla e arriva solo all'intermediario
        #NO DEBITO
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