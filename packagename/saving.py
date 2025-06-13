nb_work_hour_per_day=7           #### interface streamlit [1-7] 7 par défaut
nb_work_day_per_year=260        #### interface streamlit [1-365] 260 par défaut

ratio_invoicable=0.65   ### interface streamlit (équalizer)
ratio_admin=0.1            # ATTENTION : si modification d'un des ' ratios
ratio_prospection=0.15     # alors répartir équitablement 100% - somme(ratio_invoicable, ratio_admin, ratio_prospection, ratio_dev)
ratio_dev=0.1


leadcraftr_input_time=1 # minutes
leadcraftr_mail_time=1   # minutes
leadcraftr_nb_mail=20
std_leads_identification=60    # minutes
std_mail_time=5   #minutes
to = 40000  #euros
tjm = 300 #euros



def input_invoice_output_tjm(
            to=to,
            nb_work_hour_per_day=nb_work_hour_per_day,
            nb_work_day_per_year=nb_work_day_per_year,
            ratio_invoicable=ratio_invoicable):

    tjm = to/(nb_work_day_per_year*ratio_invoicable)
    thm= tjm/nb_work_hour_per_day
    return int(tjm), int(thm)

def input_tjm_output_invoice(
            tjm=tjm,
            nb_work_hour_per_day=nb_work_hour_per_day,
            nb_work_day_per_year=nb_work_day_per_year,
            ratio_invoicable=ratio_invoicable):

    to = nb_work_day_per_year * ratio_invoicable * tjm
    thm = tjm/nb_work_hour_per_day
    return int(to), int(thm)

def savings_time_money(nb_mails=20, tjm = tjm, nb_work_hour_per_day=nb_work_hour_per_day ):
    std_time = std_leads_identification + (nb_mails * std_mail_time)
    leadcraftr_time = leadcraftr_input_time + (nb_mails * leadcraftr_mail_time)
    time_saving = (std_time -  leadcraftr_time)
    cost_saving = time_saving/60 * tjm/nb_work_hour_per_day
    return list([time_saving, cost_saving])


turnover = float(input(" quel chiffre d'affaire facturable annuel visez vous ? : "))
print("")
print(f"Un CA de {int(turnover)} euros représente un TJM de {input_invoice_output_tjm(to=turnover)[0]} euros pour {nb_work_day_per_year} journées travaillées de {nb_work_hour_per_day}h et un taux de facturation de {ratio_invoicable*100}% ")
print(f"Ce TJM correspond à un taux horaire de {input_invoice_output_tjm(to=turnover)[1]} euros")
print("")

TxJM = int(input("Quel TJM considérez vous ? : "))
print("")
print(f"un TJM de {TxJM} euros engendre un CA de {int(input_tjm_output_invoice(tjm=TxJM)[0])} euros pour {nb_work_day_per_year} journées travaillées de {nb_work_hour_per_day}h et un taux de facturation de {ratio_invoicable*100}% ")
print("")

nb_mail = int(input("combien de mails venez vous d'envoyer ? "))
print("")
print(f"By sending {nb_mail} prospecting emails with LeadCrafte(r), you’ve just saved around {savings_time_money(nb_mail)[0]:.0f} minutes — equivalent to €{savings_time_money(nb_mail)[1]:,.2f}, based on your standard daily rate.")
print(f"Using LeadCrafte(r) weekly could help you reclaim up to {savings_time_money(nb_mails=20)[0]*52/60:.0f} hours per year — giving you more time to focus on what really matters.")
print(f"That’s approximately {savings_time_money(nb_mails=20)[0]*52/60/nb_work_hour_per_day:.0f} extra working days annually — ideal for growing your business, following up on key opportunities, or simply creating space to breathe.")
print(f"And if you convert that saved time into revenue, it could be worth as much as €{savings_time_money(nb_mails=20)[0]*52/60 * TxJM/nb_work_hour_per_day:,.2f} — a valuable return made possible by LeadCrafte(r).")
