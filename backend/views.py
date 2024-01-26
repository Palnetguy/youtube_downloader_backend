# views.py
from urllib.parse import unquote
from pytube import YouTube
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def download_yt_url(request):
    # Get the 'url' parameter from the request data
    
    url = request.data.get('url', None)
    print("Trying this:")

    if not url:
        return Response({'error': 'URL parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Decode the URL if needed
    decoded_url = unquote(url)

    try:
        yt = YouTube(decoded_url)
        list_for_options = []

        for i in yt.streams:
            item = i.__dict__
            selected_item = {
                'url': item['url'],
                'itag': item['itag'],
                'mime_type': item['mime_type'],
                'resolution': item['resolution'],
                'audio_res': item['abr']
            }

            list_for_options.append(selected_item)

        return Response(list_for_options)

    except Exception as e:
        return Response({'error': f'Error processing the YouTube video: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
