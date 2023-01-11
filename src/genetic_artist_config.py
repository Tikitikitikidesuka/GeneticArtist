from pydantic import BaseModel
import genetic_algorithm_config


class Configuration(BaseModel):
    genetic_algorithm: genetic_algorithm_config.Configuration
