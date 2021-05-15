import pandas as pd
import tensorflow as tf
import numpy as np
import cv2
from io import BytesIO
import base64
from PIL import Image

from processing import get_components
from calculator import latexEval


# path to dictnory
dest_path = '.\\savedata\\dict.csv'
df = pd.read_csv(dest_path, header=None, delimiter=',')
key = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))


#predict each component
def classify(components):
    test = np.asarray([
        components[i]['pic'] for i in sorted(components.keys())
    ]).astype(np.float32)
    dim = 45
    test = tf.reshape(test, [-1, dim, dim, 1])
    #load model
    new_model = tf.keras.models.load_model('seq_model_new.model')
    predict_results = new_model.predict(test)
    predicts = []
    for i in range(predict_results.shape[0]):
        predicts.append(np.argmax(predict_results[i]))
    for i, d in enumerate(predicts):
        components[i + 1]['label'] = d
        components[i + 1]['output'] = key[d]
    return components

# group assign 
def assign_group(components, offset_threshold=3):
    heights = []
    for i in components:
        heights.append([components[i]['tl'][0], components[i]['br'][0]])
    groups = [heights[0]]
    new_height = heights[1:]
    for height in new_height:
        # checking the next element belong to same group
        if height[0] + offset_threshold < groups[-1][1]:
            groups[-1][1] = max(height[1], groups[-1][1])
        else:
            # adding to another group
            groups.append(height)
    for i in components:
        for group in groups:
            x = group[0]
            y = group[1]
            # assign each component to a group
            if x < components[i]['tl'][0] + offset_threshold < y:
                components[i]['group'] = group
    return components, groups

# find superscript for simple numerics
def superscriptnums(newComp, components):
    l_order = sorted(newComp.keys(), key=lambda x: newComp[x]['tl'][1])
    pt, pl = newComp[l_order[0]]['tl']
    pb, pr = newComp[l_order[0]]['br']
    mid = (pb+pt)//2
    for i in range(1, len(l_order)):
        ct, cl = newComp[l_order[i]]['tl']
        cb, cr = newComp[l_order[i]]['br']
        if(cb<mid):
            components[l_order[i]]['sup'] = True

    return components

# detect superscripts based on z score and method superscriptnums
def detect_script(components, groups):
    for g in groups:
        bottoms = []
        tops = []
        for i in sorted(components.keys()):
            if(components[i]['group'] == g):
                bottoms.append(components[i]['br'][0])
                tops.append(components[i]['tl'][0])
        bottoms_mean = np.mean(bottoms)
        bottoms_std = np.std(bottoms)
        tops_mean = np.mean(tops)
        tops_std = np.std(tops)
        nums = [str(i) for i in range(10)]
        nums.append("\sqrt")
        nums.append("y")
        nums.append("z")
        operators = ['\\times', 'x', '+', '-', '\div']
        flag = 1
        new_comp = {}
        for k in sorted(components.keys(), key=lambda x: components[x]['tl'][1]):
            if components[k]['group'] == g:
                if(components[k]['output'] not in nums):
                    flag = 0
                    # components = superscriptnums(new_comp, components)
                    # new_comp = {}
                    break
                else:
                    if(components[k]['output'] != '\sqrt'):
                        new_comp[k] = components[k]
        print("flag ", flag)
        print("new com ", new_comp)
        print("new com ", new_comp.keys())
        if(flag):
            components = superscriptnums(new_comp, components)
            continue
        if(1 == len(bottoms)):
            continue
        for i in components:
            if components[i]['group'] == g:
                z_score_bottom = (bottoms_mean - components[i]['br'][0]) / bottoms_std
                z_score_top = (components[i]['tl'][0] - tops_mean) / tops_std
                s = z_score_bottom - z_score_top
                if s > 2.35:
                    components[i]['sup'] = True
    return components

# finding difference between minus and fraction line
def finffrac(components, groups):
    l_order = sorted(components.keys(), key=lambda x: components[x]['tl'][1])
    for i in range(len(l_order)):
        if (components[l_order[i]]['output'] == '-'):
            idx = i
            minus_range = [components[l_order[idx]]["tl"][1], components[l_order[idx]]["br"][1]]
            comp_range = [components[l_order[i+1]]["tl"][1], components[l_order[i+1]]["br"][1]]
            if(minus_range[0] <= comp_range[0] <= comp_range[1] <= minus_range[1] and components[l_order[idx]]['group'] == components[l_order[i+1]]['group']):                
                components[l_order[idx]]['output'] = '\\frac'    
                components[l_order[idx]]['frac'] = True            
    return components

# new order after determining numerator and denominators
def neworder(components, groups):
    components = finffrac(components, groups)
    l_order = sorted(components.keys(), key=lambda x: components[x]['tl'][1])
    order = [components[i]["output"] for i in l_order]
    num = []
    denom = []
    frac = 0
    s = []
    idx = 0
    for i in l_order:
        if(components[i]["output"] == '\\frac' and frac==0):
            s.append(i)
            idx = i
            frac = 1
            continue
        elif(frac and components[idx]['group'] == components[i]['group']):
            minus_range = [components[idx]["tl"][1], components[idx]["br"][1]]
            comp_range = [components[i]["tl"][1], components[i]["br"][1]]
            if(minus_range[0] <= comp_range[0] <= comp_range[1] <= minus_range[1] and components[idx]['group'] == components[i]['group']):
                components[i]['sup'] = False
                components[i]['sub'] = False
                if(components[idx]["tl"][0] < components[i]["tl"][0]):
                    components[i]['frac'] = True
                    components[i]['deno'] = True
                    denom.append(i)
                else:
                    components[i]['frac'] = True
                    components[i]['num'] = True
                    num.append(i)
            else:
                new_num = [components[j]["output"] for j in num]
                new_den = [components[j]["output"] for j in denom]
                frac = 0
                components[num[0]]['output'] = '{' + components[num[0]]['output']
                components[num[-1]]['output'] = components[num[-1]]['output'] + '}'
                components[denom[0]]['output'] = '{' + components[denom[0]]['output']
                components[denom[-1]]['output'] = components[denom[-1]]['output'] + '}'
                new_numCom = {}
                new_denCom = {}
                for k1 in num:
                    new_numCom[k1] = components[k1]
                components = superscriptnums(new_numCom, components)

                for k2 in denom:
                    new_denCom[k2] = components[k2]
                components = superscriptnums(new_denCom, components)

                s += num
                s += denom
                num = []
                denom = []
                s.append(i)
        else:
            s.append(i)
    if(len(num) or len(denom)):
        frac = 0
        components[num[0]]['output'] = '{' + components[num[0]]['output']
        components[num[-1]]['output'] = components[num[-1]]['output'] + '}'
        components[denom[0]]['output'] = '{' + components[denom[0]]['output']
        components[denom[-1]]['output'] = components[denom[-1]]['output'] + '}'
        new_num = [components[j]["output"] for j in num]
        new_den = [components[j]["output"] for j in denom]

        new_numCom = {}
        new_denCom = {}
        for k1 in num:
            new_numCom[k1] = components[k1]
        components = superscriptnums(new_numCom, components)

        for k2 in denom:
            new_denCom[k2] = components[k2]
        components = superscriptnums(new_denCom, components)

        s += num
        s += denom
        num = []
        denom = []
    return s

# constructing after assigning groups, superscripts and fractions
def construct_latex(components, groups):
    lr_order = sorted(components.keys(), key=lambda x: components[x]['tl'][1])
    order = []
    for i in lr_order:
        order.append(components[i]["output"])
    lr_order = neworder(components, groups)
    order = []
    for i in lr_order:
        order.append(components[i]["output"])
    vsep = {tuple(group): [] for group in groups}
    MODE_SUP = set()
    MODE_SUB = set()
    MODE_SQRT = {}
    print("components 5 ", components)
    for l in lr_order:
        t, left = components[l]['tl']
        b, right = components[l]['br']
        for g in vsep:
            if g[0] <= t and t <= b and b <= g[1]:

                if g in MODE_SQRT and left > MODE_SQRT[g]:
                    vsep[g].append('}')
                    del MODE_SQRT[g]
                if g in MODE_SUP and not components[l]['sup']:
                    vsep[g].append('}')
                    MODE_SUP.remove(g)
                if g in MODE_SUB and not components[l]['sub']:
                    vsep[g].append('}')
                    MODE_SUB.remove(g)
                if g not in MODE_SUP and components[l]['sup']:
                    vsep[g].append('^{')
                    MODE_SUP.add(g)
                if g not in MODE_SUB and components[l]['sub']:
                    vsep[g].append('_{')
                    MODE_SUB.add(g)
                vsep[g].append(components[l]['output'] + ' ')
                if components[l]['output'] == '\\sqrt':
                    MODE_SQRT[g] = right
                    vsep[g].append('{')
                break
    for i in MODE_SQRT:
        vsep[i].append('}')
    for j in MODE_SUP:
        vsep[j].append('}')
    for g in vsep:
        vsep[g] = ''.join(vsep[g])

    print("after script",vsep)
    if len(vsep) == 3:
        first_g, _, last_g = list(sorted([g for g in vsep], key=lambda g: g[0]))
        final = '\\frac{' + vsep[first_g] + '}{' + vsep[last_g] + '}'
    else:
        final = list(vsep.values())[0]
    final = final.replace(" ", "")
    final = final.replace("\lambda", "\lambda ")
    return final

# Main process
def expLatex(data):
    print("Enter")
    file_name_X1 = Image.open(BytesIO(base64.b64decode(data)))
    X_processed1 = cv2.cvtColor(np.array(file_name_X1), cv2.COLOR_BGR2GRAY)
    print("processed image shape ", X_processed1.shape)
    _, labels1 = cv2.connectedComponents(X_processed1)
    print("labeled image shape ", labels1.shape)
    components1 = get_components(labels1)
    print("Components1: ", components1)
    components2 = classify(components1)
    print("Components2: ", components2)
    components3, groups1 = assign_group(components2)
    print("Components3: ", components3)
    print("Groups : ", groups1)
    components4 = detect_script(components3, groups1)
    print("Components4: ", components4)
    expression1 = construct_latex(components4, groups1)
    print("expression : ", expression1)
    return expression1