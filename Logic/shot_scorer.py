'''Shot Scoring Module'''

import math

from Logic.Path.vectors import Vectors


class ShotScorer:
    '''Ranks candidate shots using a heuristic composite score'''

    vectors = Vectors()

    def score_shot(self, white, hit_position, target_ball, target_hole):
        '''
        Returns a score for a given shot. Lower score = better shot.

        Factors:
          - Cue-ball travel distance (shorter = better, less chance of scratch)
          - Target-ball to hole distance (shorter = better)
          - Directness penalty: angle between cue direction and target→hole direction
            (straighter alignment = easier pot)
        '''
        cue_distance = self.vectors.distance_from_two_points(white, hit_position)
        pocket_distance = self.vectors.distance_from_two_points(target_ball, target_hole)
        angle_penalty = self._angle_between_vectors(white, hit_position, target_ball, target_hole)

        return cue_distance + pocket_distance + angle_penalty * 60

    def rank_shots(self, candidates):
        '''Return candidates sorted ascending by score (best first)'''
        return sorted(candidates, key=lambda c: c['score'])

    @staticmethod
    def _angle_between_vectors(white, hit_position, target_ball, target_hole):
        '''Angle in radians between cue-ball direction and target-ball→hole direction'''
        dx1 = hit_position[0] - white[0]
        dy1 = hit_position[1] - white[1]
        dx2 = target_hole[0] - target_ball[0]
        dy2 = target_hole[1] - target_ball[1]

        mag1 = math.sqrt(dx1 ** 2 + dy1 ** 2) or 1e-9
        mag2 = math.sqrt(dx2 ** 2 + dy2 ** 2) or 1e-9

        cos_angle = max(-1.0, min(1.0, (dx1 * dx2 + dy1 * dy2) / (mag1 * mag2)))
        return math.acos(cos_angle)
