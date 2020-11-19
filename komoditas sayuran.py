import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
from collections import Counter


desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',10)

#import dataset merah
path =r'C:\Users\fikri\Desktop\pyproj\komoditas bawang\komoditas'
filenames = glob.glob(path + "\*.csv")

dfs = []
for csv in filenames:
    frame = pd.read_csv(csv)
    frame['Komoditas'] = os.path.basename(csv).split('.')[0]
    dfs.append(frame)

all_data = pd.concat(dfs, ignore_index=False)
all_data = all_data.drop(['provinsi', 'kode_kabupaten_kota','satuan'],axis=1)
all_data = all_data[all_data.jumlah_produksi != 0]
all_data['Komoditas'] = all_data['Komoditas'].str.title()
print(all_data)


#commodities visualization
data_pie = all_data.groupby('Komoditas').sum().reset_index()
data_pie = data_pie.sort_values(by='jumlah_produksi',ascending=False)
print(data_pie)

plt.rcParams['figure.figsize']=(20, 30)
plt.style.use('dark_background')

sns.catplot(x='Komoditas', y='jumlah_produksi', data=data_pie,palette = 'viridis', kind='bar', legend=True)
plt.xlabel('Komoditas', size=18, labelpad=10)
plt.ylabel('Jumlah Produksi(ton)', size=18, labelpad=10)
plt.title('Jumlah Produksi Komoditas Sayuran Jawa Barat', fontweight = 30, fontsize = 20)
plt.xticks(rotation=45, fontsize=12)
ax = plt.gca()
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d' % int(p.get_height()),
            fontsize=12, color='white', ha='center', va='bottom')

# city production visualization
city_prod = all_data.groupby('nama_kabupaten_kota')['jumlah_produksi'].sum().reset_index()
city_prod = city_prod.sort_values(by='jumlah_produksi', ascending=False)
print(city_prod)

sns.catplot(x='nama_kabupaten_kota', y='jumlah_produksi', data=city_prod,palette = 'gnuplot', kind='bar', legend=True)
plt.xlabel('Daerah', size=18, labelpad=10)
plt.ylabel('Jumlah Produksi(ton)', size=18, labelpad=10)
plt.title('Jumlah Produksi tiap Daerah di Jawa Barat', fontweight = 30, fontsize = 20)
plt.xticks(rotation=90, fontsize=12)
ax = plt.gca()
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d' % int(p.get_height()),
            fontsize=12, color='white', ha='center', va='bottom')

# most production data

kab_garut = all_data[all_data['nama_kabupaten_kota'] == 'KABUPATEN GARUT'].groupby('Komoditas')['jumlah_produksi'].sum().reset_index().sort_values(by='jumlah_produksi', ascending = False)
kab_garut['persentase'] = (kab_garut['jumlah_produksi']/kab_garut['jumlah_produksi'].sum())*100
print(kab_garut)


#Dominator's Data
city_pie = all_data.groupby(['Komoditas']).apply(lambda x: x.nlargest(3,['jumlah_produksi'])).reset_index(drop=True)
#print(city_pie)
count_wc = Counter(city_pie['nama_kabupaten_kota'])

countee = pd.DataFrame(count_wc.items(), columns=['Nama Kabupaten/Kota','Poin'])
countee = countee.sort_values('Poin', ascending=False)
print(countee)



juara = city_prod
juara['persentase'] = (city_prod['jumlah_produksi']/city_prod['jumlah_produksi'].sum())*100
print(juara.head(3))

kab_bandung = all_data[all_data['nama_kabupaten_kota'] == 'KABUPATEN BANDUNG'].groupby('Komoditas')['jumlah_produksi'].sum().reset_index().sort_values(by='jumlah_produksi', ascending = False)
kab_bandung['persentase'] = (kab_bandung['jumlah_produksi']/kab_bandung['jumlah_produksi'].sum())*100
total = kab_bandung.iloc[9:17].sum()
total = total.drop(['Komoditas'])
total['Komoditas'] = 'Lain-lain'
kab_bandung = kab_bandung.append(total.transpose(),ignore_index=True)
kab_bandung= kab_bandung.drop(kab_bandung.index[9:17])


fig1, ax1 = plt.subplots()
ax1.pie(kab_bandung['jumlah_produksi'], autopct='%1.1f%%',textprops={'color':"b"},
        startangle=90)
plt.title("Komoditas Kabupaten Bandung", fontsize=16)
ax1.axis('equal')
plt.legend(kab_bandung['Komoditas'], loc="best",fontsize=14)
#plt.show()
print(kab_bandung)


city_pie = city_pie.merge(data_pie, left_on='Komoditas',right_on='Komoditas',how="left")
city_pie['Persentase']= (city_pie['jumlah_produksi_x']/city_pie['jumlah_produksi_y'])*100
dom_data = city_pie[city_pie['nama_kabupaten_kota'] == 'KABUPATEN BANDUNG'].drop(['jumlah_produksi_y'],axis=1)
dom_data=dom_data[['Komoditas','jumlah_produksi_x','Persentase']]
dom_data=dom_data.sort_values(by='Persentase',ascending=False).reset_index(drop=True)
save = dom_data.to_csv()
print(dom_data)

# BigBro's Data
BB = ['KOTA BANDUNG' , 'KOTA BEKASI' , 'KOTA BOGOR' , 'KOTA DEPOK']
big_bro = city_prod[city_prod['nama_kabupaten_kota'].str.contains('|'.join(BB))].reset_index(drop=True)
print(big_bro)

sns.catplot(x='nama_kabupaten_kota', y='jumlah_produksi', data=big_bro,palette = 'gnuplot', kind='bar', legend=True)
plt.xlabel('Daerah', size=18, labelpad=10)
plt.ylabel('Jumlah Produksi(ton)', size=18, labelpad=10)
plt.title('Jumlah Produksi Kota Besar di Jawa Barat', fontweight = 30, fontsize = 20)
plt.xticks(rotation=30, fontsize=12)
ax = plt.gca()
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d' % int(p.get_height()),
            fontsize=12, color='red', ha='center', va='bottom')

plt.show()