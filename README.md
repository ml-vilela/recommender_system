# Recommender System

Demo app for a recommender system to marketplace. The dataset was build using
syntetic data, meaning the model evaluation is not totally possible and the 
algorithms will return fake predictions.

For the marketplace we will generate data for the two ends: side_a and side_b.
Each one represents an entity that could be translated in any other dual-side
relationship, for example, property owners and people looking for places.

Each side will have a unique set of tags, these will represent the 
characteristics of a given record, in a real-world scenario it could be, for
example, clean, bright, spacy for properties and ponctual, friendly for people.

Besides the descriptive data of each record we will also use a rating for a
set of transactions, for instance, one person stayed in a property and gave 
a rating 4 on that specific transaction. All these will be randomly generated 
and used to create predictions on the recommender system. Naturally, as this 
example is for a market place we have the side_a -> side_b and side_b -> side_a
ratings.


## Filtering methods

This example uses two filtering methods, Content Filtering and Collaborative 
Filtering.

Content filtering will find similarities between a given record in one side, 
for example, find properties or people with similar set of tags. Collaborative 
filtering, in the other hand, provides a predicted rating for a side_a - side_b 
or side_b - side_a pair.

Note that in this example we want to maximise the experience, meaning if `side_a`
record `A` gives a 5 stars rating to `side_b` record `B` and record `B` gives a
1 start rating to `A` we will penalise that transaction. To solve that the 
prediction will always be based on both sides transactions side_a->side_b and
side_b->side_a, we will use a normalized euclidean distance to generate the 
rating.

We will also provide an hybrid method, using content filtering to find similar 
records and sort them by predicted rating with collaborative filtering.

## Endpoints

The endpoints will be namespaced by the side, following by the filter method.
On the example implementation we will use `side_a` and `side_b`.

All endpoints will be reached by a `GET` request and parameters should be in
the query string.

There are three endpoints available for each namespace.

### Content Filtering

#### Request

```
GET namespace/similar_to
```
Input Parameters:

```
id
```

Output:

```
[[record_id_1, similarity_1], [record_id_2, similarity_2], [record_id_3, similarity_3], ...]
```

Example:

```
GET http://localhost:6000/side_a/similar_to?id=3
```

```
[[2806, 0.108581154288685], [4323, 0.09330194951440984], [2190, 0.083498284917634], [2823, 0.08032554819669094], [4400, 0.07720633975363259], [582, 0.07138182167211615], [3443, 0.06565894099796514], [1752, 0.05227408067761559], [2895, 0.05139938496190853], [3829, 0.05029470410650487]]
```

### Collaborative filtering

#### Request

```
GET namespace/ratings_for
```
Input Parameters:

```
id
record_ids
```

Output:

```
[[record_id_1: rating_for_1], [record_id_2: rating_for_2], [record_id_3: rating_for_3], ...]
```

Example:

```
GET http://localhost:6000/side_a/ratings_for?id=3&record_ids=423,524,765
```

```
[[423: 0.6345], [524: 0.5985], [765: 0.5723]]
```

### Hybrid

#### Request

```
GET namespace/similar_to_with_rating
```
Input Parameters:

```
id
```

Output:

```
[[record_id_1: rating_for_1], [record_id_2: rating_for_2], [record_id_3: rating_for_3], ...]
```

Example:

```
GET http://localhost:6000/side_a/similar_to_with_rating?id=3
```

```
[[423: 0.6345], [524: 0.5985], [765: 0.5723]]
```

## Generate syntetic data

I've created some scripts to generate syntetic data, there are two groups of
datasets: tags and ratings. The source for tags can be found on the file 
directory. The output will be saved in the datasets directory.

To generate the data use the script below
```
$ python scripts/generators/generate_datasets.py
```

The list is generated using the values on `modules/generators/macros.py` file.
You can override that simply updating the file.

Defaults:
- SIDE_A_COUNT: 5000
- SIDE_B_COUNT: 500
- MIN_RATING: 1
- MAX_RATING: 5
- MIN_TAGS: 5
- MAX_TAGS: 10
- MIN_REVIEWS: -10 (any value below 1 will not create a review)
- MAX_REVIEWS: 5

Note the system will generate one worker more than SIDE_A_COUNT, this
side_a record has no rating and that is done to test the hybrid filtering method.

### TODO:
Use distribution (bi-modal seems to be the most appropriated for ratings on 
this case) to generate syntetic data.


## Train the models

Train content filtering algorithm

```
$ python scripts/train/content_filtering.py
```

Train collaborative filtering algorithm

```
$ python scripts/train/collaborative_filtering.py
```

## Start the web app

```
$ python app.py
```

## Docker

The docker will build generate the syntetic data and train the models, expect
difference between each image, but it's ready to use.

```
$ docker build -t recommender .
```

```
$ docker run -p 6000:6000 recommender
```
