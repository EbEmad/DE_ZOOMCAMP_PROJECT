import pandas as pd
import os
from scripts.Fetch_Data import fetch_data
from datetime import datetime
def process_data(doc, **kwargs):
    try:
        order = []
        country = []
        population = []
        yearly_change = []
        net_change = []
        density = []
        land_area = []
        migrants = []
        fert_rate = []
        med_age = []
        urban_pop = []
        world_share = []
        ins_date = []
        whole_data = {}

        # to fetch the variable from prev function
        doc = fetch_data()

        container = doc.find_all("div", class_="not-prose")
        table_child = container[0].find_all("table")
        table_row = table_child[0].find_all("tr")

        headers = table_row[0].find_all("th")
        headers_list = [header.get_text() for header in headers]

        for row in table_row[1:]:
            row_elements = row.find_all("td")

            #order
            try:
                order.append(int(row_elements[0].get_text()))
            except:
                order.append(-1)

            # country
            try:
                country.append(str(row_elements[1].get_text()))
            except:
                country.append('N/A')

            # population
            try:
                population.append(int(row_elements[2].get_text().replace(',', '')))
            except:
                population.append(0)

            # yearly_change
            try:
                yearly_change.append(float(row_elements[3].string.strip().split(' ')[0]))
            except:
                yearly_change.append(0)

            # net_change
            try:
                net_change.append(float(row_elements[4].string.strip().replace(',', '')))
            except:
                net_change.append(0)

            # density
            try:
                density.append(int(row_elements[5].string.strip().replace(',', '')))
            except:
                density.append(0)

            # land_area
            try:
                land_area.append(float(row_elements[6].string.strip().replace(',', '')))
            except:
                land_area.append(0)

            # migrants
            try:
                migrants.append(int(row_elements[7].string.strip().replace(',', '')))
            except:
                migrants.append(0)

            # fert_rate
            try:
                fert_rate.append(float(row_elements[8].string.strip()))
            except:
                med_age.append(0)

            # med_age
            try:
                med_age.append(int(row_elements[9].string.strip()))
            except:
                med_age.append(0)

            # urban_pop
            try:
                urban_pop.append(int(row_elements[10].string.strip().split(' ')[0]))
            except:
                urban_pop.append(0)

            # world_share
            try:
                world_share.append(float(row_elements[11].string.strip().split(' ')[0]))
            except:
                world_share.append(0)

            # inserted_date
            ins_date.append(str(datetime.now()))

        ziped_lists = list(zip(order, country, population, yearly_change, net_change, density, land_area, migrants, fert_rate, med_age, urban_pop, world_share, ins_date))
    
        try:
            whole_data.clear()
            order.clear()
            country.clear()
            population.clear()
            yearly_change.clear()
            net_change.clear()
            density.clear()
            land_area.clear()
            migrants.clear()
            fert_rate.clear()
            med_age.clear()
            urban_pop.clear()
            world_share.clear()
            ins_date.clear()
        except:
            raise Exception("Can't clear the lists!")
        else:
            print("Lists are clear!")
    
        try:
            for o, c, p, y, n, d, l, m, f, g, u, w, t in ziped_lists:
                order.append(o)
                country.append(c)
                population.append(p)
                yearly_change.append(y)
                net_change.append(n)
                density.append(d)
                land_area.append(l)
                migrants.append(m)
                fert_rate.append(f)
                med_age.append(g)
                urban_pop.append(u)
                world_share.append(w)
                ins_date.append(t)
        except:
            raise Exception("Can't add data into lists!")
        else:
            print('Lists are full of data!')

        whole_data = {
            f"{headers_list[1].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : country,
            f"{headers_list[2].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : population,
            f"{headers_list[3].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : yearly_change,
            f"{headers_list[4].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : net_change,
            f"{headers_list[5].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : density,
            f"{headers_list[6].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : land_area,
            f"{headers_list[7].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : migrants,
            f"{headers_list[8].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : fert_rate,
            f"{headers_list[9].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : med_age,
            f"{headers_list[10].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : urban_pop,
            f"{headers_list[11].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : world_share,
            'INS_DATE': ins_date
        }

        # create pandas dataframe for data
        df = pd.DataFrame(data=whole_data)

        print("Data processing complete.")
        return df
    except Exception as e:
        raise Exception("Error processing data:", e) from e