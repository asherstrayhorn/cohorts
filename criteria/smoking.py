


def smoke(something):
    pass




"""     so, major contributors to good performance were:
            -  organize the document in such a way that relevant sections can be extracted
            -  for extracted sections:
                -  choose token level features and whatever other features that seem relevant (e.g. entities, diagnoses, etc)
                -  either combine each section from a document or perform a classification for each section
            -  train a machine learning model
            -  use some kind of postprocessing rules to correct obvious mistakes or determine preferred labels when there are collisions

"""