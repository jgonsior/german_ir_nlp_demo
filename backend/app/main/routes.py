from random import randint
from flask import request, jsonify
from . import bp


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

        return jsonify(response)


@bp.route('/document/', methods=['GET'])
def get_document():
    if request.method == 'GET':
        document_id = request.args.get('id')
        print(document_id, flush=True)
        return jsonify({"page": [
                              {
                                "headers": ["Biographie","Kindheit"],
                                "passage": "Harry Potter wurde am 31. Juli 1980 als Sohn von James und Lily Potter, Mitglieder des ersten Orden des Phönix, während des Höhepunkts des ersten Krieges, geboren. Von Geburt an lebte er mit seinen Eltern in einem ausgesuchten Versteck, da Lord Voldemort Harry töten wollte. Sie lebten in dem Dorf Godric's Hollow in einem Haus, das unter dem Fidelius-Zauber stand. Als Teil des Zaubers hatten sie geplant, Sirius Black zu ihrem Geheimniswahrer zu machen, aber auf seinen Rat hin entschieden sie sich letztendlich doch für Peter Pettigrew, da dieser vermeintlich weniger verdächtigt werden würde, über die Potters Bescheid zu wissen. Pettigrew, der sich als Spion Voldemorts herausstellte, verriet die Familie. Er täuschte seinen eigenen Tod vor und schob Sirius die Schuld für seinen, den von 12 unschuldigen Muggeln und den Tod der Potters in die Schuhe.",
                              }
                            ]})
