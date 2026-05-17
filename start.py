'''Start Module'''

import argparse

from Logic.options import Options
from Logic.video_analysis import VideoAnalysis


def create_parser():
    '''Responsible for creating a parser that handles program arguments'''

    formatter = lambda prog: argparse.HelpFormatter(prog, width=140, max_help_position=50)

    parser = argparse.ArgumentParser(
        description='8-Ball Pool analysis bot. Runs on recorded footage (default) or live screen capture (--live).',
        formatter_class=formatter,
        add_help=False
    )

    # Detection parameters
    parser.add_argument('-br', '--ball_radius',    metavar='N',    type=int, nargs=1, default=[10],     help='Radius of the pool balls in pixels.')
    parser.add_argument('-hr', '--hole_radius',    metavar='N',    type=int, nargs=1, default=[20],     help='Radius of the table holes in pixels.')
    parser.add_argument('-bd', '--border_distance', metavar='N',   type=int, nargs=1, default=[15],     help='Distance from hole centre to table edge.')
    parser.add_argument('-tb', '--target_balls',   metavar='type', type=str, nargs=1, default=['solid'],
                        choices=['solid', 'striped'], help='Ball type to target: solid or striped.')
    parser.add_argument('-sf', '--skip_frame',     metavar='N',    type=int, nargs=1, default=[10],     help='Process every N-th frame.')

    # Video mode (offline)
    parser.add_argument('-ip', '--input_video',    metavar='file', type=str, nargs=1, default='Footage\\Example_01.mp4',
                        help='Input video file (*.mp4). Used when --live is not set.')
    parser.add_argument('-op', '--output_video',   metavar='file', type=str, nargs=1, default='Footage\\Output.mp4',
                        help='Output video file (*.mp4).')
    parser.add_argument('-save', '--save_video',   action='store_true', help='Save annotated video output.')

    # Display
    parser.add_argument('-show', '--show_video',   action='store_true', help='Show annotated frames while processing.')

    # Live mode
    parser.add_argument('--live',    action='store_true',
                        help='Enable live screen-capture mode instead of reading a video file.')
    parser.add_argument('-m', '--monitor', metavar='N', type=int, nargs=1, default=[1],
                        help='Monitor index for screen capture (1 = primary). Used with --live.')
    parser.add_argument('-reg', '--region', metavar='N', type=int, nargs=4, default=None,
                        help='Capture region: LEFT TOP WIDTH HEIGHT in pixels. Overrides -m when set.')

    # Shot execution
    parser.add_argument('-exec', '--execute', action='store_true',
                        help='Execute shots automatically via pyautogui. Requires --live.')
    parser.add_argument('-delay', '--delay', metavar='N', type=float, nargs=1, default=[3.0],
                        help='Minimum seconds between automated shots (default 3.0).')

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    options = Options(args)
    video_analysis = VideoAnalysis()

    if options.live_mode:
        video_analysis.analyse_live(options)
    else:
        video_analysis.analyse_video(options)
