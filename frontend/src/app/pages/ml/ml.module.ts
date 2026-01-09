import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { MlComponent } from './ml.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: MlComponent }
];

@NgModule({
  declarations: [
    MlComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class MlModule { }
