# scripts/core/complete_retrieval.py

import time
from typing import Callable, List, Dict, Optional
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


class CompleteRetrieval:
    """
    Universal pagination engine for complete result retrieval
    - Fetches ALL available results (no truncation)
    - Newest papers first (2024 → 2015)
    - User confirmation for large result sets (>15,000)
    """

    def __init__(self, config):
        self.config = config
        self.retrieval_settings = config.get("retrieval_settings", {})
        self.threshold = self.retrieval_settings.get("user_confirmation_threshold", 15000)
        self.order = self.retrieval_settings.get("order", "newest_first")

    def fetch_all(
        self,
        api_function: Callable,
        query: str,
        database: str,
        year_range: tuple = (2015, 2024),
        batch_size: int = 200
    ) -> List[Dict]:
        """
        Fetch ALL results with automatic handling of large datasets

        Args:
            api_function: API wrapper function
            query: Search query
            database: Database name
            year_range: (start_year, end_year)
            batch_size: Papers per request

        Returns:
            List of all papers (newest first)
        """

        logger.info(f"\n{'='*60}")
        logger.info(f"📡 Fetching from {database.upper()}")
        logger.info(f"{'='*60}")

        # Step 1: Get total count
        total = self._get_total_count(api_function, query, database)

        if total == 0:
            logger.warning(f"⚠️ No results found for query")
            return []

        logger.info(f"📊 Total results: {total:,}")

        # Step 2: Check if user confirmation needed
        if total > self.threshold:
            total, query = self._handle_large_results(
                total, query, database, year_range, api_function
            )

            if total == 0:  # User cancelled
                return []

        # Step 3: Fetch all papers (newest first)
        papers = self._fetch_paginated(
            api_function, query, database, total, batch_size, year_range
        )

        logger.info(f"✅ {database}: {len(papers):,} papers retrieved\n")
        return papers

    def _get_total_count(self, api_function, query, database):
        """Get total result count from API"""
        try:
            response = api_function(query, start=0, count=1)
            return self._extract_total(response, database)
        except Exception as e:
            logger.error(f"Error getting total count: {e}")
            return 0

    def _extract_total(self, response, database):
        """Extract total from API response"""
        if database == "scopus":
            return int(response.get("search-results", {}).get("opensearch:totalResults", 0))
        elif database == "openalex":
            return response.get("meta", {}).get("count", 0)
        elif database == "semantic_scholar":
            return response.get("total", 0)
        elif database == "arxiv":
            # arXiv doesn't provide total, need to fetch all
            return 10000  # Arbitrary high number
        else:
            return 0

    def _handle_large_results(self, total, query, database, year_range, api_function):
        """
        Handle large result sets with user confirmation
        Suggest year cutoff to reduce papers
        """

        print(f"\n{'='*60}")
        print(f"⚠️  LARGE RESULT SET: {database.upper()}")
        print(f"{'='*60}")
        print(f"\nTotal results: {total:,}")
        print(f"User confirmation threshold: {self.threshold:,}")

        # Get year distribution
        year_dist = self._estimate_year_distribution(
            query, database, year_range, api_function
        )

        print(f"\n📊 Estimated distribution by year (newest first):")
        print("-" * 60)

        cumulative = 0
        for year in range(year_range[1], year_range[0] - 1, -1):
            count = year_dist.get(year, 0)
            cumulative += count
            if count > 0:
                print(f"  {year}: {count:>6,} papers  (cumulative: {cumulative:>7,})")

        # Suggest cutoff
        suggested_year = self._suggest_cutoff(year_dist, self.threshold, year_range)
        suggested_count = sum(
            count for year, count in year_dist.items()
            if year >= suggested_year
        )

        print(f"\n💡 RECOMMENDATION:")
        print(f"   Limit to papers from {suggested_year} onwards")
        print(f"   → Would retrieve ~{suggested_count:,} papers")
        print(f"   → Focuses on recent/relevant research")

        print(f"\n{'='*60}")
        print(f"❓ OPTIONS:")
        print(f"   1. Retrieve ALL {total:,} papers (may take hours)")
        print(f"   2. Limit to {suggested_year}+ (~{suggested_count:,} papers) [RECOMMENDED]")
        print(f"   3. Custom year cutoff")
        print(f"   4. Cancel this database")
        print(f"{'='*60}\n")

        choice = input("Your choice (1-4): ").strip()

        if choice == "1":
            logger.info("✓ User chose: Retrieve ALL papers")
            return total, query

        elif choice == "2":
            logger.info(f"✓ User chose: Limit to {suggested_year}+")
            # Update query with year filter
            modified_query = self._add_year_filter(query, suggested_year, year_range[1], database)
            return suggested_count, modified_query

        elif choice == "3":
            custom_year = int(input("Enter year cutoff (YYYY): ").strip())
            custom_count = sum(
                count for year, count in year_dist.items()
                if year >= custom_year
            )
            logger.info(f"✓ User chose: Custom cutoff {custom_year}+ (~{custom_count:,} papers)")
            modified_query = self._add_year_filter(query, custom_year, year_range[1], database)
            return custom_count, modified_query

        else:  # choice == "4" or invalid
            logger.info("✓ User cancelled this database")
            return 0, query

    def _estimate_year_distribution(self, query, database, year_range, api_function):
        """
        Estimate paper distribution by year
        (Makes quick API calls to get counts)
        """
        logger.info("📊 Estimating year distribution...")

        year_dist = {}

        for year in range(year_range[0], year_range[1] + 1):
            year_query = self._add_year_filter(query, year, year, database)

            try:
                response = api_function(year_query, start=0, count=1)
                count = self._extract_total(response, database)
                year_dist[year] = count
                time.sleep(0.2)  # Rate limiting
            except:
                year_dist[year] = 0

        return year_dist

    def _suggest_cutoff(self, year_dist, threshold, year_range):
        """Suggest year cutoff to stay under threshold"""
        cumulative = 0

        # Start from newest year
        for year in range(year_range[1], year_range[0] - 1, -1):
            cumulative += year_dist.get(year, 0)

            if cumulative >= threshold:
                # Return previous year to stay under threshold
                return year + 1

        # If all years under threshold, return start year
        return year_range[0]

    def _add_year_filter(self, query, start_year, end_year, database):
        """Add year filter to query (database-specific)"""
        if database == "scopus":
            return f"{query} AND PUBYEAR >= {start_year} AND PUBYEAR <= {end_year}"
        elif database == "openalex":
            # Assume query already has filter parameter
            return query  # Filter handled separately in API call
        elif database == "semantic_scholar":
            return query  # Year handled in API parameters
        elif database == "arxiv":
            # arXiv uses date range in API call
            return query
        else:
            return query

    def _fetch_paginated(self, api_function, query, database, total, batch_size, year_range):
        """Fetch all results with pagination (newest first)"""

        all_papers = []

        # For databases with year-based ordering
        if self.order == "newest_first":
            papers = self._fetch_newest_first(
                api_function, query, database, total, batch_size, year_range
            )
        else:
            papers = self._fetch_standard(
                api_function, query, database, total, batch_size
            )

        return papers

    def _fetch_newest_first(self, api_function, query, database, total, batch_size, year_range):
        """Fetch papers year by year (newest first)"""

        all_papers = []

        with tqdm(total=total, desc=f"Fetching {database}", unit="papers") as pbar:

            # Iterate years newest to oldest
            for year in range(year_range[1], year_range[0] - 1, -1):
                year_query = self._add_year_filter(query, year, year, database)

                # Fetch all papers for this year
                start = 0
                while True:
                    try:
                        response = api_function(year_query, start=start, count=batch_size)
                        papers = self._extract_papers(response, database)

                        if not papers:
                            break

                        all_papers.extend(papers)
                        pbar.update(len(papers))

                        start += batch_size

                        # Rate limiting
                        self._rate_limit(database)

                    except Exception as e:
                        logger.warning(f"Error fetching {database} year {year}: {e}")
                        break

        return all_papers

    def _fetch_standard(self, api_function, query, database, total, batch_size):
        """Standard pagination (when year ordering not supported)"""

        all_papers = []

        with tqdm(total=total, desc=f"Fetching {database}", unit="papers") as pbar:

            start = 0
            while start < total:
                try:
                    response = api_function(query, start=start, count=batch_size)
                    papers = self._extract_papers(response, database)

                    if not papers:
                        break

                    all_papers.extend(papers)
                    pbar.update(len(papers))

                    start += batch_size

                    # Rate limiting
                    self._rate_limit(database)

                except Exception as e:
                    logger.warning(f"Error at offset {start}: {e}")
                    break

        return all_papers

    def _extract_papers(self, response, database):
        """Extract papers from API response"""
        if database == "scopus":
            return response.get("search-results", {}).get("entry", [])
        elif database == "openalex":
            return response.get("results", [])
        elif database == "semantic_scholar":
            return response.get("data", [])
        elif database == "arxiv":
            return response.get("entries", [])
        else:
            return []

    def _rate_limit(self, database):
        """Apply database-specific rate limiting"""
        delays = {
            "scopus": 0.5,
            "openalex": 0.1,
            "semantic_scholar": 0.01,
            "arxiv": 3.0,
            "web_of_science": 0.5
        }
        time.sleep(delays.get(database, 0.5))
