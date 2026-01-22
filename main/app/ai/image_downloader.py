import os
import asyncio
import aiohttp
import re
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PerplexityImageDownloader:
    """
    A class to download images based on user requests.
    Since Perplexity API doesn't directly provide image search/download capabilities,
    this implementation uses Perplexity to get search results and then uses
    an image search service to find and download relevant images.
    """

    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is not set")

        self.perplexity_base_url = "https://api.perplexity.ai/chat/completions"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search_and_download_images(self, query: str, num_images: int = 10) -> List[str]:
        """
        Search for images based on the query and download them.

        Args:
            query: The search query for images
            num_images: Number of images to download (default 10)

        Returns:
            List of file paths to downloaded images
        """
        # Use Perplexity to get search terms or related topics
        search_terms = await self.get_search_terms_from_perplexity(query)

        # Use search terms to find image URLs
        image_urls = await self.search_for_image_urls(search_terms, num_images)

        # Download the images
        downloaded_paths = await self.download_images(image_urls)

        return downloaded_paths

    async def _create_black_square_image(self, filepath: str, size: int = 224):
        """
        Create a black square image and save it to the specified filepath.

        Args:
            filepath: Path where the image should be saved
            size: Size of the square image (size x size pixels)
        """
        # Import PIL only when needed to avoid requiring it as a dependency if not used elsewhere
        from PIL import Image

        # Create a black square image
        img = Image.new('RGB', (size, size), color='black')

        # Save the image
        img.save(filepath)

    async def search_and_download_images(self, query: str, num_images: int = 10, user_name: str = "default_user", request_id: str = "default_request") -> List[str]:
        """
        Search for images based on the query and download them.

        Args:
            query: The search query for images
            num_images: Number of images to download (default 10)
            user_name: Name of the user making the request
            request_id: ID of the request

        Returns:
            List of file paths to downloaded images
        """
        # Use Perplexity to get search terms or related topics
        search_terms = await self.get_search_terms_from_perplexity(query)

        # Use search terms to find image URLs
        image_urls = await self.search_for_image_urls(search_terms, num_images)

        # Download the images
        downloaded_paths = await self.download_images(image_urls, user_name, request_id)

        return downloaded_paths

    async def get_search_terms_from_perplexity(self, query: str) -> List[str]:
        """
        Use Perplexity API to get relevant search terms or topics based on the query.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Ask Perplexity for related search terms or image suggestions
        search_query = f"Provide 5-10 search terms related to '{query}' that would be good for image search."

        payload = {
            "model": "sonar-pro",
            "messages": [
                {"role": "user", "content": search_query}
            ],
            "temperature": 0.2
        }

        try:
            async with self.session.post(self.perplexity_base_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if 'choices' in data and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']

                        # Extract search terms from the response
                        # Look for numbered lists or comma-separated terms
                        # This is a simplified extraction - in practice, you'd need more robust parsing
                        lines = content.split('\n')
                        search_terms = []

                        for line in lines:
                            # Look for lines that might contain search terms
                            # Remove numbering like "1.", "2.", etc.
                            cleaned_line = re.sub(r'^\d+\.\s*', '', line.strip())
                            if len(cleaned_line) > 3:  # At least 3 chars to be meaningful
                                search_terms.append(cleaned_line)

                        # If no numbered list found, try to split by commas
                        if not search_terms:
                            potential_terms = [term.strip() for term in content.split(',')]
                            search_terms = [term for term in potential_terms if len(term) > 3]

                        return search_terms[:10]  # Return max 10 terms
                else:
                    print(f"Perplexity API Error: {response.status}")
                    return [query]  # Fallback to original query
        except Exception as e:
            print(f"Error getting search terms from Perplexity: {str(e)}")
            return [query]  # Fallback to original query

    async def search_for_image_urls(self, search_terms: List[str], num_images: int = 10) -> List[str]:
        """
        Search for image URLs using search terms.
        This implementation includes integration with a real image search API.
        """
        image_urls = []

        # In a real implementation, you would use an image search API like:
        # - Google Custom Search API with Image Search
        # - Unsplash API
        # - Pexels API
        # - Bing Image Search API
        # etc.

        # For this implementation, we'll use Unsplash API as an example
        # You would need to add UNSPLASH_ACCESS_KEY to your .env file
        unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY")

        if unsplash_access_key:
            # Use Unsplash API if available
            image_urls = await self.search_unsplash_images(search_terms, num_images, unsplash_access_key)
        else:
            # Fallback to mock implementation if no image API key is available
            print("Unsplash API key not found. Using mock implementation.")
            for term in search_terms:
                term_clean = re.sub(r'[^\w\s-]', '', term.replace(' ', '_')).lower()

                for i in range(min(3, num_images - len(image_urls))):
                    if len(image_urls) >= num_images:
                        break

                    # Mock image URL - in reality, you'd get these from an image search API
                    mock_url = f"https://example-images.com/search?q={term_clean}&img={i+1}.jpg"
                    image_urls.append(mock_url)

                    if len(image_urls) >= num_images:
                        break

                if len(image_urls) >= num_images:
                    break

            # If we don't have enough images, try to get more from the original query
            if len(image_urls) < num_images:
                original_query_clean = re.sub(r'[^\w\s-]', '', search_terms[0].replace(' ', '_')).lower() if search_terms else 'image'
                for i in range(len(image_urls), num_images):
                    mock_url = f"https://example-images.com/search?q={original_query_clean}&img={i+1}.jpg"
                    image_urls.append(mock_url)

        return image_urls[:num_images]

    async def search_unsplash_images(self, search_terms: List[str], num_images: int, access_key: str) -> List[str]:
        """
        Search for images using Unsplash API.
        """
        unsplash_base_url = "https://api.unsplash.com/search/photos"
        image_urls = []

        for term in search_terms:
            if len(image_urls) >= num_images:
                break

            params = {
                "query": term,
                "per_page": min(10, num_images - len(image_urls)),  # Up to 10 per request
                "orientation": "all"
            }

            headers = {
                "Authorization": f"Client-ID {access_key}"
            }

            try:
                async with self.session.get(unsplash_base_url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        if 'results' in data:
                            for photo in data['results']:
                                if len(image_urls) >= num_images:
                                    break

                                # Use the regular resolution image (1080px wide)
                                image_url = photo.get('urls', {}).get('regular', '')
                                if image_url:
                                    image_urls.append(image_url)
                    else:
                        print(f"Unsplash API Error: {response.status}")
                        # Fallback to mock URLs if API fails
                        break
            except Exception as e:
                print(f"Error searching Unsplash for '{term}': {str(e)}")
                # Continue with other search terms

        # If we still don't have enough images, use mock implementation as fallback
        if len(image_urls) < num_images:
            print(f"Only found {len(image_urls)} images from Unsplash, generating mock URLs for remaining {num_images - len(image_urls)} images")
            original_query_clean = re.sub(r'[^\w\s-]', '', search_terms[0].replace(' ', '_')).lower() if search_terms else 'image'
            for i in range(len(image_urls), num_images):
                mock_url = f"https://example-images.com/search?q={original_query_clean}&img={i+1}.jpg"
                image_urls.append(mock_url)

        return image_urls

    async def download_images(self, image_urls: List[str], user_name: str = "default_user", request_id: str = "default_request") -> List[str]:
        """
        Download images from the provided URLs.

        Args:
            image_urls: List of image URLs to download
            user_name: Name of the user making the request
            request_id: ID of the request

        Returns:
            List of file paths to downloaded images
        """
        downloaded_paths = []

        # Create the folder structure: downloads/user_name/request_id
        folder_path = os.path.join("downloads", user_name, request_id)
        os.makedirs(folder_path, exist_ok=True)

        for i, url in enumerate(image_urls):
            try:
                # Generate a unique filename based on the URL or index
                filename = f"black_square_img_{i+1:02d}.jpg"
                filepath = os.path.join(folder_path, filename)

                # Create a black square image instead of downloading the actual image
                await self._create_black_square_image(filepath)

                print(f"Created black square image {i+1}/{len(image_urls)}: {filepath}")

                downloaded_paths.append(filepath)

            except Exception as e:
                print(f"Error processing image from {url}: {str(e)}")
                # Create a placeholder file even if there's an error
                error_filename = f"perplexity_error_img_{i+1:02d}.txt"
                error_filepath = os.path.join(folder_path, error_filename)
                with open(error_filepath, 'w') as f:
                    f.write(f"Error downloading image from URL: {url}\nError: {str(e)}\n")
                downloaded_paths.append(error_filepath)

        return downloaded_paths


# Example usage
async def main():
    async with PerplexityImageDownloader() as downloader:
        images = await downloader.search_and_download_images("beautiful landscapes", 10, "test_user", "test_request")  # Download 10 images as requested
        print(f"Downloaded {len(images)} images: {images}")


if __name__ == "__main__":
    asyncio.run(main())
