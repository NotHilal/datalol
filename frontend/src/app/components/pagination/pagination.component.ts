import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent {
  @Input() currentPage: number = 1;
  @Input() totalPages: number = 1;
  @Input() pageSize: number = 20;
  @Input() totalItems: number = 0;
  @Output() pageChange = new EventEmitter<number>();

  targetPage: number | null = null;

  get pages(): number[] {
    const pages: number[] = [];
    const maxVisible = 7;

    if (this.totalPages <= maxVisible) {
      for (let i = 1; i <= this.totalPages; i++) {
        pages.push(i);
      }
    } else {
      if (this.currentPage <= 4) {
        for (let i = 1; i <= 5; i++) pages.push(i);
        pages.push(-1); // ellipsis
        pages.push(this.totalPages);
      } else if (this.currentPage >= this.totalPages - 3) {
        pages.push(1);
        pages.push(-1); // ellipsis
        for (let i = this.totalPages - 4; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        pages.push(1);
        pages.push(-1); // ellipsis
        for (let i = this.currentPage - 1; i <= this.currentPage + 1; i++) {
          pages.push(i);
        }
        pages.push(-1); // ellipsis
        pages.push(this.totalPages);
      }
    }

    return pages;
  }

  get startItem(): number {
    return (this.currentPage - 1) * this.pageSize + 1;
  }

  get endItem(): number {
    return Math.min(this.currentPage * this.pageSize, this.totalItems);
  }

  onPageChange(page: number) {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.pageChange.emit(page);
    }
  }

  goToFirstPage() {
    this.onPageChange(1);
  }

  goToLastPage() {
    this.onPageChange(this.totalPages);
  }

  goToPreviousPage() {
    this.onPageChange(this.currentPage - 1);
  }

  goToNextPage() {
    this.onPageChange(this.currentPage + 1);
  }

  jumpPages(amount: number) {
    const newPage = this.currentPage + amount;
    this.onPageChange(newPage);
  }

  jumpToPage() {
    if (this.targetPage && this.isValidPage()) {
      this.onPageChange(this.targetPage);
      this.targetPage = null; // Clear input after jump
    }
  }

  isValidPage(): boolean {
    return this.targetPage !== null &&
           this.targetPage >= 1 &&
           this.targetPage <= this.totalPages &&
           this.targetPage !== this.currentPage;
  }
}
