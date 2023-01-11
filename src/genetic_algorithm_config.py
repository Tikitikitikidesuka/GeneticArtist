from pydantic import validator, BaseModel, StrictInt


class Configuration(BaseModel):
    generations: StrictInt
    population_size: StrictInt
    keep_elitism: StrictInt
    mutation_probability: float

    @validator('generations', 'population_size')
    def int_greater_than_zero(cls, value):
        if value <= 0:
            raise ValueError('value must be greater than zero')
        return value

    @validator('keep_elitism')
    def elitism_between_zero_and_population_size(cls, value, values):
        if value < 0:
            raise ValueError('value must be zero or greater')
        if value >= values['population_size']:
            raise ValueError('value must be smaller than population_size')
        return value

    @validator('mutation_probability')
    def probability_in_range(cls, value):
        if not 0 <= value <= 1:
            raise ValueError('value must be between 0.0 and 1.0')
        return value
