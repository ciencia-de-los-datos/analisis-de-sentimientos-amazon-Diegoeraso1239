"""
Análisis de Sentimientos usando Naive Bayes
-----------------------------------------------------------------------------------------

El archivo `amazon_cells_labelled.txt` contiene una serie de comentarios sobre productos
de la tienda de amazon, los cuales están etiquetados como positivos (=1) o negativos (=0)
o indterminados (=NULL). En este taller se construirá un modelo de clasificación usando
Naive Bayes para determinar el sentimiento de un comentario.

"""
import numpy as np
import pandas as pd


def pregunta_01():
    df = pd.read_csv(
        "amazon_cells_labelled.tsv",
        sep="\t",
        header=None,
        names=["msg","lbl"],
    )

    df_tagged = df[df["lbl"].notnull()]
    df_untagged = df[df["lbl"].isnull()]

    x_tagged = df_tagged["msg"]
    y_tagged = df_tagged["lbl"]

    x_untagged = df_untagged["msg"]
    y_untagged = df_untagged["lbl"]

    # Retorne los grupos de mensajes
    return x_tagged, y_tagged, x_untagged, y_untagged


def pregunta_02():
    

    
    from sklearn.model_selection import train_test_split

    
    x_tagged, y_tagged, x_untagged, y_untagged = pregunta_01()

   
    x_train, x_test, y_train, y_test = train_test_split(
        x_tagged,
        y_tagged,
        test_size=0.1,
        random_state=12345,
    )

    # Retorne `X_train`, `X_test`, `y_train` y `y_test`
    return x_train, x_test, y_train, y_test

def pregunta_03():
   
    
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    
    stemmer = PorterStemmer()

   
    analyzer = CountVectorizer().build_analyzer()

    
    return lambda x: (stemmer.stem(w) for w in analyzer(x))

def pregunta_04():
    """
    Especificación del pipeline y entrenamiento
    -------------------------------------------------------------------------------------
    """

    # Importe CountVetorizer
    # Importe GridSearchCV
    # Importe Pipeline
    # Importe BernoulliNB
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.naive_bayes import BernoulliNB
    

    
    x_train, x_test, y_train, y_test = pregunta_02()

    # Obtenga el analizador de la pregunta 3.
    analyzer = pregunta_03()

    # Cree una instancia de CountVectorizer que use el analizador de palabras
    # de la pregunta 3. Esta instancia debe retornar una matriz binaria. El
    # límite superior para la frecuencia de palabras es del 100% y un límite
    # inferior de 5 palabras. Solo deben analizarse palabras conformadas por
    # letras.
    countVectorizer = CountVectorizer(
        analyzer=analyzer,
        lowercase=True,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
        binary=True,
        max_df=1.0,
        min_df=5,
    )

  
    pipeline = Pipeline(
        steps=[
            ("CountVectorizer", countVectorizer),
            ("BernoulliNB", BernoulliNB()),
        ],
    )

    
    param_grid = {
        "BernoulliNB__alpha": np.array((0.1, 1, 10)),
    }

    
    gridSearchCV = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
        refit=True,
        return_train_score=False,
    )

    
    gridSearchCV.fit(x_train, y_train)

    
    return gridSearchCV


def pregunta_05():
    """
    Evaluación del modelo
    -------------------------------------------------------------------------------------
    """

    # Importe confusion_matrix
    from sklearn.metrics import confusion_matrix

    gridSearchCV = pregunta_04()


    X_train, X_test, y_train, y_test = pregunta_02()

   
    cfm_train = confusion_matrix(
        y_true=y_train,
        y_pred=gridSearchCV.predict(X_train),
    )

    cfm_test = confusion_matrix(
        y_true=y_test,
        y_pred=gridSearchCV.predict(X_test),
    )


    return cfm_train, cfm_test


def pregunta_06():
    """
    Pronóstico
    -------------------------------------------------------------------------------------
    """

    # Obtenga el pipeline de la pregunta 3.
    gridSearchCV = pregunta_04()

    # Cargue los datos generados en la pregunta 01.
    X_tagged, y_tagged, X_untagged, y_untagged = pregunta_01()

    # pronostique la polaridad del sentimiento para los datos
    # no etiquetados
    y_untagged_pred = gridSerchCV.predict(X_untagged)

    # Retorne el vector de predicciones
    
    return y_untagged_pred
