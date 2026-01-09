import { Component, Input, OnInit, OnChanges } from '@angular/core';
import { ChampionService } from '../../services/champion.service';

interface RoleCount {
  role: string;
  count: number;
  color: string;
  champions: string[];
}

interface DamageBalance {
  physical: number;
  magic: number;
  mixed: number;
}

interface CompositionAnalysis {
  roleCounts: RoleCount[];
  damageBalance: DamageBalance;
  diversityScore: number;
  hasTank: boolean;
  hasSupport: boolean;
  balanced: boolean;
  warnings: string[];
}

@Component({
  selector: 'app-team-composition',
  templateUrl: './team-composition.component.html',
  styleUrls: ['./team-composition.component.scss']
})
export class TeamCompositionComponent implements OnInit, OnChanges {
  @Input() participants: any[] = [];
  @Input() teamName: string = 'Team';

  composition: CompositionAnalysis | null = null;

  constructor(private championService: ChampionService) {}

  ngOnInit() {
    this.analyzeComposition();
  }

  ngOnChanges() {
    this.analyzeComposition();
  }

  /**
   * Analyze team composition
   */
  analyzeComposition() {
    if (!this.participants || this.participants.length === 0) {
      this.composition = null;
      return;
    }

    // Count roles
    const roleMap = new Map<string, string[]>();

    this.participants.forEach(p => {
      const championName = p.champion?.name;
      if (championName) {
        const role = this.championService.getChampionRole(championName);
        if (!roleMap.has(role)) {
          roleMap.set(role, []);
        }
        roleMap.get(role)!.push(championName);
      }
    });

    // Convert to array
    const roleCounts: RoleCount[] = Array.from(roleMap.entries()).map(([role, champions]) => ({
      role,
      count: champions.length,
      color: this.championService.getRoleColor(role),
      champions
    })).sort((a, b) => b.count - a.count);

    // Calculate damage balance
    const damageBalance = this.calculateDamageBalance(roleCounts);

    // Calculate diversity score (0-100)
    const diversityScore = this.calculateDiversityScore(roleCounts);

    // Check for tank and support
    const hasTank = roleMap.has('Tank');
    const hasSupport = roleMap.has('Support');

    // Check if balanced (no role has more than 2 champions)
    const balanced = roleCounts.every(rc => rc.count <= 2);

    // Generate warnings
    const warnings = this.generateWarnings(roleCounts, hasTank, hasSupport, balanced);

    this.composition = {
      roleCounts,
      damageBalance,
      diversityScore,
      hasTank,
      hasSupport,
      balanced,
      warnings
    };
  }

  /**
   * Calculate damage type balance
   */
  calculateDamageBalance(roleCounts: RoleCount[]): DamageBalance {
    let physical = 0;
    let magic = 0;
    let mixed = 0;

    roleCounts.forEach(rc => {
      switch (rc.role) {
        case 'ADC':
        case 'Assassin':
          physical += rc.count;
          break;
        case 'Mage':
          magic += rc.count;
          break;
        case 'Fighter':
        case 'Tank':
          mixed += rc.count;
          break;
        case 'Support':
          // Supports vary, count as mixed
          mixed += rc.count;
          break;
      }
    });

    const total = physical + magic + mixed;
    return {
      physical: total > 0 ? Math.round((physical / total) * 100) : 0,
      magic: total > 0 ? Math.round((magic / total) * 100) : 0,
      mixed: total > 0 ? Math.round((mixed / total) * 100) : 0
    };
  }

  /**
   * Calculate team diversity score (0-100)
   * Higher score = more diverse team composition
   */
  calculateDiversityScore(roleCounts: RoleCount[]): number {
    if (roleCounts.length === 0) return 0;

    // Ideal: 5 different roles, each with 1 champion
    // Score based on:
    // - Number of unique roles (40 points)
    // - Even distribution (40 points)
    // - Has tank and support (20 points)

    // Unique roles score (max 40)
    const uniqueRolesScore = Math.min(roleCounts.length / 5, 1) * 40;

    // Distribution score (max 40) - penalize if any role has more than 2
    const maxCount = Math.max(...roleCounts.map(rc => rc.count));
    const distributionScore = maxCount <= 1 ? 40 : maxCount === 2 ? 30 : 20;

    // Tank/Support bonus (max 20)
    const hasTank = roleCounts.some(rc => rc.role === 'Tank');
    const hasSupport = roleCounts.some(rc => rc.role === 'Support');
    const essentialScore = (hasTank ? 10 : 0) + (hasSupport ? 10 : 0);

    return Math.round(uniqueRolesScore + distributionScore + essentialScore);
  }

  /**
   * Generate composition warnings
   */
  generateWarnings(roleCounts: RoleCount[], hasTank: boolean, hasSupport: boolean, balanced: boolean): string[] {
    const warnings: string[] = [];

    if (!hasTank) {
      warnings.push('No Tank - Team lacks frontline');
    }

    if (!hasSupport) {
      warnings.push('No Support - Limited utility and healing');
    }

    if (!balanced) {
      const overloadedRole = roleCounts.find(rc => rc.count > 2);
      if (overloadedRole) {
        warnings.push(`Too many ${overloadedRole.role}s (${overloadedRole.count})`);
      }
    }

    // Check for missing damage types
    const hasPhysical = roleCounts.some(rc => rc.role === 'ADC' || rc.role === 'Assassin');
    const hasMagic = roleCounts.some(rc => rc.role === 'Mage');

    if (!hasPhysical) {
      warnings.push('Low physical damage');
    }

    if (!hasMagic) {
      warnings.push('Low magic damage');
    }

    // All AD or all AP warning
    if (roleCounts.length === 1 && (roleCounts[0].role === 'ADC' || roleCounts[0].role === 'Mage')) {
      warnings.push('One-dimensional damage type');
    }

    return warnings;
  }

  /**
   * Get score color based on diversity score
   */
  getScoreColor(): string {
    if (!this.composition) return '#95a5a6';

    const score = this.composition.diversityScore;
    if (score >= 80) return '#2ecc71'; // Green - Excellent
    if (score >= 60) return '#f39c12'; // Orange - Good
    if (score >= 40) return '#e67e22'; // Dark orange - Fair
    return '#e74c3c'; // Red - Poor
  }

  /**
   * Get score label
   */
  getScoreLabel(): string {
    if (!this.composition) return 'N/A';

    const score = this.composition.diversityScore;
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  }
}
