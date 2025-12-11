import { Component, OnInit } from '@angular/core';
import { MatchService } from '../../services/match.service';

@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.scss']
})
export class MatchesComponent implements OnInit {
  matches: any[] = [];
  loading = false;
  currentPage = 1;
  pageSize = 20;
  totalMatches = 0;
  totalPages = 0;

  constructor(private matchService: MatchService) {}

  ngOnInit() {
    this.loadMatches();
  }

  loadMatches() {
    this.loading = true;
    this.matchService.getMatches(this.currentPage, this.pageSize).subscribe({
      next: (response: any) => {
        this.matches = response.items;
        this.totalMatches = response.pagination.total;
        this.totalPages = response.pagination.totalPages;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading matches:', error);
        this.loading = false;
      }
    });
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.loadMatches();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
