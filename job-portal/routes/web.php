<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;

Route::get('/', function () {
	return view('welcome');
});

Route::middleware(['auth'])->group(function () {
	Route::get('/dashboard', function () {
		$user = auth()->user();
		if ($user->hasRole('admin')) {
			return redirect()->route('admin.dashboard');
		}
		if ($user->hasRole('recruiter')) {
			return redirect()->route('recruiter.dashboard');
		}
		return redirect()->route('seeker.dashboard');
	})->name('dashboard');

	Route::get('/seeker', function () {
		return view('dashboards.seeker');
	})->name('seeker.dashboard');

	Route::middleware(['role:recruiter'])->group(function () {
		Route::get('/recruiter', function () {
			return view('dashboards.recruiter');
		})->name('recruiter.dashboard');
	});

	Route::middleware(['role:admin'])->group(function () {
		Route::get('/admin', function () {
			return view('dashboards.admin');
		})->name('admin.dashboard');

		// Admin management routes can be added here later
	});
});
