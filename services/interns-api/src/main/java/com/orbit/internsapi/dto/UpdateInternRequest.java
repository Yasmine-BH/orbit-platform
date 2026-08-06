package com.orbit.internsapi.dto;

import com.orbit.internsapi.entity.InternStatus;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;

public record UpdateInternRequest(

        @NotBlank(message = "firstName is required")
        String firstName,

        @NotBlank(message = "lastName is required")
        String lastName,

        @NotBlank(message = "email is required")
        @Email(message = "email must be a valid address")
        String email,

        @NotBlank(message = "university is required")
        String university,

        @NotNull(message = "startDate is required")
        LocalDate startDate,

        @NotNull(message = "status is required")
        InternStatus status
) {
}
