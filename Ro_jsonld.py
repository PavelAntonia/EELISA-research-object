import properties as p
import json

class ro_jsonld(object):

    def __init__(self):

        self.jsonld = {}
        self.jsonld["@context"] = "https://w3id.org/ro/crate/1.1/context"
        self.graph = [
            {
                "@type": "CreativeWork",
                "@id": "ro-crate-metadata.json",
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
                "about": {"@id": "./"},
                "description": "RO-Crate Metadata File Descriptor (this file)"
            },
            {
                "@id": "./",
                "@type": "Dataset",
                "name": "",
                "description": "",
                "author": [],
                "hasPart": []
            }
        ]


    def load_data(self, data):

        self.data = data

        self.graph_add_title(self.data.title)

        # Self creates the hardcoded structure for paper
        if self.data.type == "paper":
            self.graph_add_description(self.data.summary)
            self.graph_add_authors(self.data.authors)
            self.graph_add_softwares(self.data.software)
            self.graph_add_datasets(self.data.datasets)
        
        # Self creates the hardcoded structure for project
        if self.data.type == "project":
            self.graph_add_description(self.data.goal)
            self.graph_add_authors(self.data.authors)
            self.graph_add_softwares(self.data.software)
            self.graph_add_datasets(self.data.datasets)
            self.graph_add_demo(self.data.demo)

        # Adds graph to the final structure jsonld
        self.jsonld["@graph"] = self.graph


    def _normalize_name(self, name):
        """Normalizes names in order to be used as an ID."""
        return "#" + str(name).replace(' ', '_').lower()


    def _add_id_to_list(self, name, list):
        """Enters a name with blank spaces or not and appends
        to the list a id normalized version of the name. List 
        must be a list of dicts."""

        id_normalized = self._normalize_name(name)
        list.append({
            "@id": id_normalized
        })

    def graph_add_title(self, title):

        if title is None:
            return None
        
        self.graph[1]["name"] = title

    def graph_add_demo(self, demo):

        if demo is None:
            return None

        workExample_list = []
        for d in demo:
            workExample_list.append(
                {
                    "@type": "Demo",
                    "link": d.link,
                    "name": d.name,
                    "description": d.description

                })
        self.graph.append({ "workExample": workExample_list })
            


    def graph_add_description(self, description):

        if description is None:
            return

        self.graph[1]["description"] = description


    def graph_add_authors(self, authors):

        if authors is None:
            return

        for author in authors:

            self._add_id_to_list(author.name, self.graph[1]["author"])

            self.graph.append({
            "@id": self._normalize_name(author.name),
            "@type": "Person",
            "name": author.name,
            "position": author.position.split(", "),
            "description": author.description
        })

    def graph_add_softwares(self, softwares):

        if softwares is None:
            return

        for software in softwares:

            self._add_id_to_list(software.name, self.graph[1]["hasPart"])

            self.graph.append({
            "@id": self._normalize_name(software.name),
            "installUrl": software.link,
            "@type": "SoftwareApplication",
            "description": software.description
        })


    def graph_add_datasets(self, datasets):

        if datasets is None:
            return
        
        for dataset in datasets:

            self._add_id_to_list(dataset.name, self.graph[1]["hasPart"])

            self.graph.append({
                "@id": self._normalize_name(dataset.name),
                "@type": "Dataset",
                "name": dataset.name,
                "description": dataset.description,
                "distribution": {"@id": dataset.link}
            })


    def create_JSONLD_file(self):
        # dump changes into output/ro-crate.json
        with open(self.data.output_jsonld, "w+") as file:
            file.write(json.dumps(self.jsonld, indent=4, sort_keys=True))
        print(f"JSON-LD file created at {self.data.output_jsonld}")
        

