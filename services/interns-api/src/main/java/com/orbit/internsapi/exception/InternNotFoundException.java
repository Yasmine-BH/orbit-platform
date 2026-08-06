package com.orbit.internsapi.exception;

public class InternNotFoundException extends RuntimeException {

    public InternNotFoundException(Long id) {
        super("Intern not found with id " + id);
    }
}
