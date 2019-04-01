r = open("resultsLenna512.csv","w")
r.write("Cluster, Support, ClTime, MineTime, EnTime, CoTime, DeTime, ClTableSize, CoTableSize, CoImSize, Actual Size, TotalSize, JPEG Size, CR, CRP(w.r.t Actual), CR(w.r.t JPEG), Total Time, Our PSNR, JPEG PSNR\n")
with open("results.txt","r") as p:
	for line in p:
		a = line.replace("\n","").split("-")
		cr = (786.6/(float(a[21])/1000))
		crpa = ((786.6 - float(a[21])/1000)/786.6)*100
		crpj = ((404-float(a[21])/1000)/404)*100
		r.write(str(a[1])+","+str(a[3])+","+str(a[5])+","+str(a[7])+","+str(a[9])+","+str(a[11])+","+str(a[13])+","+str(a[15])+","+str(float(a[17])/1000)+","+str(float(a[19])/1000)+","+str("786.6")+","+str(a[21])+","+str("404")+","+str(cr)+","+str(crpa)+","+str(crpj)+","+str(a[23])+" , \n")
		