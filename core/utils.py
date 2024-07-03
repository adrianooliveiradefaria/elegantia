from typing import Dict


class Nomalizacao:
    """
    Métodos para normalização de dados como ObjetcId, datas, números.

    Atributes:
        Nenhum.

    Methods:
        id_documento(documento):
            Converte um ObjectId {_id} do MongoDB em string.
    """

    def id_documento(self, documento: Dict):
        """
        Normaliza o campo {_id} (ObjectId) de um documento MongoDB para adequá-lo ao {id} do Schema que é str.

        Parameters:
            documento (Dict): Documento retornado pelo MongoDB utilizando a biblioteca {motor}.

        Returns:
            Dict: Documento com o {_id} convertido para str na variável {id} e o {_id} (ObjectId) excluindo.

        Raises:

        Examples:

        """
        if '_id' in documento:
            documento['id'] = str(documento['_id'])
            del documento['_id']
        return documento


normalizacao = Nomalizacao()
