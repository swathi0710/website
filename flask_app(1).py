from flask import Flask
from flask import request
import pandas as pd
import pickle
#from flask import render_template

#load model:
with open('model.pkl', 'rb') as handle:
    model = pickle.load(handle)


app = Flask(__name__)

@app.route('/')
def homepage():
    website = '''
<!DOCTYPE html>
<html>

<body>
    <style>
      a:link {
      color: #9e0340;
      background-color:#eae7e8;
       }

      a:visited {
      color: #9e0340;
      background-color:#eae7e8;
      }
      body {
        background-image: url("https://raw.githubusercontent.com/swathi0710/AIML_project_ingredient-analyser/main/cartt.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        color:#003333;
      }
    </style>

    <h1>Ingredient Analyser</h1>
    <ul>
        <li><a href="/result">Classifier</a></li>
        <li><a href="/samples">Sample ingredients</a></li>
    </ul>
    <br>
    <br>
    <br>



    <h2>Useful links</h2>
    <p>
    <ul><li><a href="https://www.fda.gov/consumers/consumer-updates/how-safe-are-color-additives">Safety of Artificial colors per the FDA</a></li>
        <li><a href="https://www.bbc.com/future/article/20190311-what-are-nitrates-in-food-side-effects">Information about Nitrites and nitrates</a></li>
        <li><a href="https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/artificial-sweeteners/art-20046936">Artificial Sweeteners</a></li>
        <li><a href="https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/in-depth/trans-fat/art-20046114">Effects of Trans Fat</a></li>
        <li><a href="https://health.clevelandclinic.org/avoid-the-hidden-dangers-of-high-fructose-corn-syrup-video/">High Fructose Corn Syrup</a></li>
        <li><a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6062396/">Research about toxicology of flavoring agents</a></li>
        </ul>
    </p>
</body>
</html>'''
    return website

@app.route('/result')
def my_form():
    website = '''
<!DOCTYPE html>
<html>
<body>
    <style>
      body {
        background-image: url("https://raw.githubusercontent.com/swathi0710/AIML_project_ingredient-analyser/main/gradient.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        color:orange;
        text-align: center;
      }
    </style>
    <h1>Classifier</h1>
    <h2>Enter the list of ingredients here</h2>
    <form action="result" method="POST">
        <input type="text" name="ingredients">
        <input type="submit" value="Classify">
    </form>
</body>
</html>'''
    return website

@app.route('/samples')
def sample():
    website = '''
<!DOCTYPE html>
<html>
<body>
    <style>
      body {
        background-image: url("https://raw.githubusercontent.com/swathi0710/AIML_project_ingredient-analyser/main/gradient.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        color:black;
      }
    </style>
    <h1>Sample Ingredients to test the tool</h1>
    <table border="1" bgcolor="#92A8D1">
    <th>Product</th>
    <th>Ingredient List</th>

    <tr><td>Lays</td><td>Potato, Edible Vegetable Oil (Palmolein Oil, Rice Bran Oil), Sugar (5.5%), Starch, lodised Salt, "Spices & Condiments (Garlic Powder, Onion Powder, Chilli), Cocoa Solids, Milk Solids. CONTAINS ADDED FLAVOUR (NATURAL, NATURE IDENTICAL &ARTIFICIAL (SOY SAUCE) FLAVOURING SUBSTANCES) "Used a natural flavouring agent. POTATO CHIPS PROPRIETARY FOOD" Limited perod offer valid in select geographies only.
</td></tr>
    <tr><td>Gummy Bears(House of Candy)</td><td>Sugar, glucose syrup,water, gelatine, acid:E330, meltodextrin, flavouring,colour: E100, E120, E141, E160e; vegetables oils (palm kernel, coconut), glazing agents: beeswax, carnauba wax</td></tr>
    <tr><td>Kapiva Amla Juice</td><td>Each 100ml contains: Amla (Emblica Officinacle) fr. fruit: 100ml Excipient - Ascorbic Acid: 100mg Permitted Class II Preservatives: Sodium Benzoate QS</td></tr>
    <tr><td>Tropicana Orange Juice</td><td>100% PURE ORANGE JUICE FROM CONCENTRATE (FILTERED WATER AND CONCENTRATED ORANGE JUICE) AND NATURAL FLAVORS. Ingredient Statement: 100% APPLE JUICE FROM CONCENTRATE (FILTERED WATER AND CONCENTRATED APPLE JUICE), NATURAL FLAVORS, MALIC ACID AND ASCORBIC ACID (VITAMIN C).</td></tr>
    <tr><td>Britannia Nutri Choice Biscuits></td><td>Refined Wheat Flour, Whole Wheat Flour, Edible Vegetable Oil (Palm), Sugar, Wheat Bran, Liquid Glucose, Milk Solids, Maltodextrin, Raising Agents, Iodised Salt, Emulsifiers, Malt Extract & Dough Conditioner.</td></tr>
    </table>
    <a href="/result">Go to classifier</a>

</body>
</html>'''
    return website


@app.route('/result', methods=['POST'])
def my_form_post():
    ingredients = request.form['ingredients']
    A_C=any([key in ingredients for key in ["color","colour","yellow","blue","green","red"]])
    nn=any([key in ingredients for key in ["nitrite","nitrate"]])
    sw=any([key in ingredients for key in ['aspartame','sucralose','acesulfame K','acesulfame','saccharin','xylitol','sweetener','neotame']])
    tf=any([key in ingredients for key in ["hydrogenated","hydrogenated oil","hydrogenated soy","trans fat"]])
    hf=any([key in ingredients for key in ['high fructose corn syrup','corn syrup','hf']])
    ff=any([key in ingredients for key in ['fragrance','flavor','flavour','scent']])

    map={k:v for k,v in zip(["Artificial_colour","Nitrites_Nitrates","HighFructoseCornSyrup","Trans_Fat","Fragrance_Flavor","Artificial_Sweetener"],[A_C,nn,hf,tf,ff,sw])}

    X=pd.DataFrame(map,index=range(5))

    res=model.predict(X)
    p=res[0]
    m={1:"May contain relatively high amounts of harmful additives.",
2: "Contains relatively harmful additives.",
3: "Additives are harmful to be consumed on a regular basis.",
4: "Relatively few additives are present.",
5: "Relatively safe"}

    page='''
<!DOCTYPE html>
<html>
<body background="https://raw.githubusercontent.com/swathi0710/AIML_project_ingredient-analyser/main/gradient.jpg" text="orange" alignment=center>

    <h1>Class:{}</h1>
    <h2>{}</h2>


</body>
</html>'''.format(p,m[p])

    return page




if __name__ == '__main__':
    app.run()