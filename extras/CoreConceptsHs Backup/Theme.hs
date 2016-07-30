-- the base concept of a theme
-- defining non-spatial and non-temporal thematic (a.k.a. attribute) values and operations on them
-- (c) Werner Kuhn
-- latest change: Jan 15, 2016

module Theme where

-- thematic values
-- essentially measurement scales
-- modeled as a sum type (until we need more)
-- any generic behavior across scales? probably just equality (almost by definition)
data Value = Boolean Bool | Nominal String | Ordinal String | Interval Int | Ratio Float deriving (Eq, Show)

