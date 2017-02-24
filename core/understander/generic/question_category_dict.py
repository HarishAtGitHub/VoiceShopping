question_category = {'what': 'what',
                     #'where': 'where', as it is handled by map
                     'why': 'why',
                     'who': 'who',
                     'when' : 'when',
                     'how many': 'quantity',
                     'how much': 'quantity',
                     'are': 'boolean',
                     'can': 'boolean',
                     'will': 'boolean',
                     }

# keeping it separate to prioritize questions
question_markers = ['what', 'when',
                    #'where', as it is handled by map
                    'why', 'who', 'how many', 'how much', 'will', 'can', 'are']