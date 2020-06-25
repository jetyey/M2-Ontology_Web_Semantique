from wtforms import StringField, SelectField
from flask_wtf import FlaskForm
from flask import Flask, render_template
import rdflib

def realCategory(inputString):
	if(inputString=="Furniture"):
		return "http://linkedgeodata.org/page/ontology/Furniture"

	elif(inputString=="Jewelry"):
		return "http://linkedgeodata.org/page/ontology/Jewelry"
	
	elif(inputString=="Shoes"):
		return "http://linkedgeodata.org/page/ontology/Apparel"

	elif(inputString=="Garden & Patio"):
		return "http://linkedgeodata.org/page/ontology/Outdoor"

	elif(inputString=="Baby Gear"):
		return "http://linkedgeodata.org/ontology/BabyShop"

	elif(inputString=="Christmas"):
		return "http://linkedgeodata.org/ontology/Decoration"

	elif(inputString=="Housewares"):
		return "http://projectontovmi.com/Home_Improvement"

	elif(inputString=="Rugs"):
		return "http://caressesrobot.org/ontology#Kitchenware"

	elif(inputString=="Bedding Basics"):
		return "https://schema.org/bed"

	elif(inputString=="Beauty Products"):
		return "http://www.disit.org/km4city/schema#HealthCare"

	elif(inputString=="Cameras & Camcorders"):
		return "http://projectontovmi.com/High_Tech"
	
	elif(inputString=="Kitchen & Dining"):
		return "http://caressesrobot.org/ontology#Kitchenware"

	return "none"


def query_sparql(input_string,tri,categorie):
    
    if(categorie=="Tous"):
        categorie=""
    elif(categorie=="Apparel"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Apparel> ."
    elif(categorie=="Baby Shop"):
        categorie = "?inst a <http://linkedgeodata.org/ontology/BabyShop> ."
    elif(categorie=="Bed"):
        categorie = "?inst a <https://schema.org/bed> ."
    elif(categorie=="Decoration"):
        categorie = "?inst a <http://linkedgeodata.org/ontology/Decoration> ."
    elif(categorie=="Food"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Food> ."
    elif(categorie=="Furniture"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Furniture> ."
    elif(categorie=="Garage"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Garage> ."
    elif(categorie=="Health care"):
        categorie = "?inst a <http://www.disit.org/km4city/schema#HealthCare> ."
    elif(categorie=="High Tech"):
        categorie = "?inst a <http://projectontovmi.com/High_Tech> ."
    elif(categorie=="Home Improvement"):
        categorie = "?inst a <http://projectontovmi.com/Home_Improvement> ."
    elif(categorie=="Jewelry"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Jewelry> ."
    elif(categorie=="Kitchenware"):
        categorie = "?inst a <http://caressesrobot.org/ontology#Kitchenware> ."
    elif(categorie=="Office"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Office> ."
    elif(categorie=="Outdoor"):
        categorie = "?inst a <http://linkedgeodata.org/page/ontology/Outdoor> ."
    
    else:
        categorie=""



    if(tri == "pa"):
        tri = "ASC(?price)"
    elif(tri== "pd"):
        tri = "DESC(?price)"
    elif(tri== "na"):
        tri = "ASC(?score)"
    elif(tri== "nd"):
        tri = "DESC(?score)"
    g = rdflib.Graph()
    g.parse("ontology.owl", format="json-ld")
    name = "\""+input_string+"\""
    if(input_string==""):
        name = ""
    else:
        name = "filter contains(lcase(?name),"+name+")" 

    results = g.query("""
    PREFIX s:   <http://schema.org/>
    PREFIX vmi: <http://projectontovmi.com/>
    PREFIX lov: <http://linkedgeodata.org/page/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl:<http://www.w3.org/2002/07/owl#>

SELECT ?name ?price ?score ?report  WHERE {

    """+categorie+"""
    ?inst vmi:hasName ?name.
    ?inst vmi:hasPrice ?price .
    ?inst vmi:hasDescription ?description .
    ?inst vmi:isTheProductOf ?review.
    ?review vmi:hasScore ?score .
    ?review vmi:hasReview ?report .
    """+name+""" 
}ORDER BY """+tri+"""


""")

    stroun = "<ul>"
    for row in results:
        stroun += "<p><li><b>Name:</b></li>  %s <li><b>Price:</b></li>  %s <li><b>Score:</b></li>  %s <li><b>Review:</b></li>  %s </p>" % row
    
    stroun+="</ul>"
    return stroun






app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret'


class LoginForm(FlaskForm):
    searchfield = StringField('Nom du produit: ')
    choices = [('Tous','Tous'),('Apparel', 'Apparel'),
               ('Baby Shop', 'Baby Shop'),
               ('Bed', 'Bed'),
               ('Decoration', 'Decoration'),
               ('Food', 'Food'),
               ('Furniture', 'Furniture'),
               ('Garage', 'Garage'),
               ('Health care', 'Health care'),
               ('High Tech', 'High Tech'),
               ('Home Improvement', 'Home Improvement'),
               ('Jewelry', 'Jewelry'),
               ('Kitchenware', 'Kitchenware'),
               ('Office', 'Office'),
               ('Outdoor', 'Outdoor'),
               ]
    price = [('Ascendant', 'Ascendant'),
               ('Descendant', 'Descendant')]
    tri = [('pa', 'Prix (ascendant)'),
               ('pd', 'Prix (descendant)'),
               ('na', 'Notes (ascendant)'),
               ('nd', 'Notes (descendant)')]
    catselect = SelectField('Catégorie:', choices=choices)
    triselect = SelectField('Trier par:',choices=tri)


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if(form.validate_on_submit()):
        #form.catselect.data
        return query_sparql(form.searchfield.data,form.triselect.data,form.catselect.data)
        
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
