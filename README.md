## Interactions Recoverability

This is a small tool I wrote to test whether a _Focused Reading_ pathway is recoverable.

It casts a _directed graph_ with the interactions found in the _SQLite_ database with _REACH_-extracted interactions and
 looks for the existence of a path between the constituen interactions in a training/testing pathway used by the FR code.
 
 To run it use `main.py` with the first argument being the data file and the second being the path to the interactions'
  database.  