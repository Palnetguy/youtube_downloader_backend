# views.py
from urllib.parse import unquote
from django.http import HttpResponse
from pytube import YouTube, Stream, monostate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def health_check(request):
    return HttpResponse("OK", status=200)


@api_view(['POST'])
def download_yt_url(request):
    url = request.data.get('url', None)

    if not url:
        return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

    decoded_url = unquote(url)

    try:
        yt = YouTube(decoded_url)

        # Extract information from the video and each stream
        video_info = {
            'title': yt.title,
            'channel_name': yt.author,
            'thumbnail_url': yt.thumbnail_url,
            'duration': yt.length,
            'streams': [],
            # 'audio_trials':[]
        }

        # Collect streams with audio information
        # streams_with_audio = [stream for stream in yt.streams if 'abr' in stream.__dict__ == ""]
        # print(streams_with_audio)

        # default_audio_stream =  next(iter(streams_with_audio), None)
        # print(default_audio_stream.__dict__['abr'])
        # streams_with_audio = []

        for stream in yt.streams:
            item = stream.__dict__
            # video_info['audio_trials'].append({"url": item['url'],'audio_res': item['abr']} if item['abr'] != None else print(video_info['audio_trials'][0]['audio_res']))

            selected_item = {
                'url': item['url'],
                'itag': item['itag'],
                'mime_type': item['mime_type'],
                'resolution': item['resolution'],
                'audio_res': item['abr'],
                'audio_codec': item['audio_codec'],
                'size': stream.filesize,
            }
            video_info['streams'].append(selected_item)
        # print(streams_with_audio)

        return Response(video_info)

    except Exception as e:
        return Response({'error': f'Error processing the YouTube video: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
