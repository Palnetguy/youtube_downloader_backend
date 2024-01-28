# views.py
from urllib.parse import unquote
from pytube import YouTube, Stream, monostate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#  @api_view(['POST'])
# def download_yt_url(request):
#     # Get the 'url' parameter from the request data
    
#     url = request.data.get('url', None)
#     print("Trying this:")

#     if not url:
#         return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

#     # Decode the URL if needed
#     decoded_url = unquote(url)

#     try:
#         yt = YouTube(decoded_url)
        
#         print(yt)
#         info = Stream(yt.streams, yt.stream_monostate)
#         print(info)
#         list_for_options = []

#         for i in yt.streams:
#             item = i.__dict__
#             selected_item = {
#                 'url': item['url'],
#                 'itag': item['itag'],
#                 'mime_type': item['mime_type'],
#                 'resolution': item['resolution'],
#                 'audio_res': item['abr'],
#                 # 'title': item['title'],
#                 # 'thumbnail_url': item['thumbnail_url']
#             }
            

#             list_for_options.append(selected_item)

#         return Response(list_for_options)

#     except Exception as e:
#         return Response({'error': f'Error processing the YouTube video: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def download_yt_url(request):
    # Get the 'url' parameter from the request data
    url = request.data.get('url', None)

    if not url:
        return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Decode the URL if needed
    decoded_url = unquote(url)

    try:
        yt = YouTube(decoded_url)

        # Extract information from the video and each stream
        video_info = {
            'title': yt.title,
            'channel_name': yt.author,
            'thumbnail_url': yt.thumbnail_url,
            'duration': yt.length,
            'streams': []
        }

        for stream in yt.streams:
            # Filter streams based on mime_type
            # if stream.mime_type.startswith('video/mp4') or stream.mime_type.startswith('audio/mp4'):
            # stream_info = {
            #     'url': stream.url,
            #     'itag': stream.itag,
            #     'mime_type': stream.mime_type,
            #     'resolution': stream.resolution,
            #     'audio_res': stream.abr,
            #     'size': stream.filesize,  # Size of the video
            # }
            item = stream.__dict__
            selected_item = {
                'url': item['url'],
                'itag': item['itag'],
                'mime_type': item['mime_type'],
                'resolution': item['resolution'],
                'audio_res': item['abr'],
                'size': stream.filesize,
            }
            video_info['streams'].append(selected_item)

        return Response(video_info)

    except Exception as e:
        return Response({'error': f'Error processing the YouTube video: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
