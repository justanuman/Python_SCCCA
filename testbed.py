"""def automatic_testing_RA():
    G = nx.Graph()
    raw_vert=[i for i in range(0,20)]
    for i in range(10):
        for_net=[]
        raw_a=[]
        raw_s=[]
        raw_r=[]
        raw_ra=[]
        for i in range(20):
            c= random.randint(0,19)
            v=random.randint(0,19)
            if(c==v):
                while (c==v):
                    c= random.randint(0,19)
                    v=random.randint(0,19)
                a=[c,v]
                b= {c,v}
                raw_ra.append(a)
                raw_a.append(a)
                raw_s.append(a)
                raw_r.append(a)
                
                for_net.append(b)
            else:
                a=[c,v]
                b= {c,v}
                raw_ra.append(a)
                raw_a.append(a)
                raw_s.append(a)
                raw_r.append(a)
                
                for_net.append(b)
        G.add_edges_from(for_net)

        etalon=list(nx.connected_components(G))
        etalon=cleanup(etalon)
        #clean_S=cleanup(S.Algorithm_S([s for s in range(0,20)], raw_s))
        #print(clean_S)
        #print("Alg_R")
        #clean_R=cleanup(R.AlgorithmR([r for r in range(0,20)], raw_r))
        #print(clean_R)
        #print("Alg_A")
        #clean_A=cleanup(A.Algorithm_A([a for a in range(0,20)], raw_a))
        #print(clean_A)
        clean_RA=cleanup(RA.AlgorithmRA([ra for ra in range(0,20)], raw_ra))
        #print("Alg_RA")
        #print(clean_RA)
        
        """assert compare(clean_R, etalon), 
        assert compare(clean_A, etalon), 
        assert compare(clean_S, etalon), 
        assert compare(clean_RA, etalon), """
        """if(not (compare(clean_R, etalon))):
            print ("input")
            print(((str(for_net)).replace("{","[")).replace("}","]"))
            print("mistake alg R")
            print(etalon)
            print(clean_R)
            #иногда сравнение ломается если порядок различается
            #разберусь чуть позже
            print("_______")
        elif(not compare(clean_A, etalon)):
            print ("input")
            print(((str(for_net)).replace("{","[")).replace("}","]"))
            print("mistake alg A")
            print(etalon)
            print(clean_A)
            print("_______")
        elif(not compare(clean_S, etalon)):
            print ("input")
            print(((str(for_net)).replace("{","[")).replace("}","]"))
            print("mistake alg S")
            print(etalon)
            print(clean_S)
            print("_______")"""
        if(not compare(clean_RA, etalon)):
            print ("input")
            print(((str(for_net)).replace("{","[")).replace("}","]"))
            print("mistake alg RA")
            print(etalon)
            print(clean_RA)
            print("_______")
        G.clear()
"""