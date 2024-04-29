from random import randint
from flask import request, jsonify
from . import bp
from .generate_random_results import Randomizer


randomizer = Randomizer()

@bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        print(query, flush=True)
        response = {
            "search_id": randint(0, 100),
            "answers": [
                {
                    "rank": 0,
                    "document_id": randint(0, 100),
                    "document_name": "Harry Potter",
                    "categorie": "sample",
                    "authors": ["Harry Fan", "Ron Fan"],
                    "passages": [
                        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                },
                {
                    "rank": 1,
                    "document_id": randint(0, 100),
                    "document_name": "Ron Weasley",
                    "categorie": "",
                    "authors": ["Ron Fan"],
                    "passages": [
                        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                }
            ]
        }

<<<<<<< HEAD
        return randomizer.get_result()
||||||| fa59faa
        return 'Your search results'


=======
        return jsonify(response)


@bp.route('/document/', methods=['GET'])
def get_document():
    if request.method == 'GET':
        document_id = request.args.get('id')
        print(document_id, flush=True)
        return jsonify("""{{Infobox Zauberstab
|Bild=[[Datei:Scabior's wand.JPG|250px]]
|Name=Scabiors Zauberstab
|hideh=
|Hersteller=[[Garrick Ollivander]] (möglich)
|Hergestellt=
|Meister=*[[Scabior]]
*[[Bellatrix Lestrange]] (möglich)
|Besitzer=[[Scabior]]
|hidem=m
|Holz=
|Kern=
|Länge=
|Eigenschaften=
}}
{{Dialog a-b|Scabior|Was soll das denn, Frau?|Bellatrix Lestrange| ''Stupor''! ''Stupor''!|[[Scabior]] richtete seinen Zauberstab auf [[Bellatrix Lestrange]] und wurde danach [[Schockzauber|geschockt]].|Harry Potter und die Heiligtümer des Todes (Buch)}}
Der '''Zauberstab''' von [[Scabior]] ist von unbekannter Länge und aus unbekanntem Holz- und Kernmaterial.

==Geschichte==
Wie die meisten [[Zauberschaft|Zauberer und Hexen]] in [[Großbritannien]] erwarb er ihn wahrscheinlich im Alter von elf Jahren, bevor er seine Ausbildung in den magischen Künsten begann.

Scabior benutzte ihn während seiner Pflichten als [[Greifer]] und während eines kurzen Duells mit [[Bellatrix Lestrange]] während des [[Gefecht im Landsitz der Familie Malfoy|Gefechtes im Landsitz der Familie Malfoy]]. &lt;ref name="Buch 723"&gt;''[[Harry Potter und die Heiligtümer des Todes (Buch)]]'' - Kapitel 23 (''Das Haus Malfoy'')&lt;/ref&gt;

==Hinter den Kulissen==
*Es ist unbekannt, was mit Scabior geschah, nachdem er von [[Bellatrix Lestrange]] geschockt wurde, aber der Dialog lässt vermuten, dass sie beabsichtigte, ihn später zu töten. Falls das der Fall war, ist es möglich, dass der Zauberstab seine Gefolgschaft auf Bellatrix übertragen hat.
**Diese Annahme wird unterstützt, da Scabior in der Verfilmung des zweiten Teils von Heiligtümer des Todes mit einem anderen Zauberstab gesehen wird kurz vor seinem Tod in der Schlacht von Hogwarts.
*Dieser Zauberstab besitzt viele Kampfspuren, was vermuten lässt, dass Scabior in vielen Duellen gekämpft hat. Allerdings kann angenommen werden, dass das Holz in dieser Form geschnitzt als einzigartiges Design.
[[Datei:ScabiorDifferenceWand.JPG|thumb|200px|Scabior mit einem anderen Zauberstab]]
*In ''[[Harry Potter und die Heiligtümer des Todes (Film 2)]]'' wird Scabiors Zauberstab mit einem hellbraunen Griff und einem glatten schwarzen Schaft gezeigt im Gegensatz zum [[Noble Collection|Noble]]-Zauberstab, der komplett schwarz gezeigt wird mit einer seltsamen Textur, die stark an kohleähnliches Material erinnert.

==Auftritte==
*''[[Harry Potter und die Heiligtümer des Todes (Buch)]]'' {{Erster}}
*''[[Harry Potter und die Heiligtümer des Todes (Film 1)]]''
*''[[Harry Potter und die Heiligtümer des Todes (Spiel 1)]]''
*''[[Harry Potter und die Heiligtümer des Todes (Film 2)]]''
*''[[Harry Potter und die Heiligtümer des Todes (Spiel 2)]]''
*''[[LEGO Harry Potter: Jahre 5 - 7]]''

==Anmerkungen und Quellen==
{{Reflist}}

[[en:Scabior's wand]]
[[Kategorie:Scabiors Besitztümer|Zauberstab]]
[[Kategorie:Zauberstäbe]]""")
>>>>>>> origin/frontend-add-data-service
