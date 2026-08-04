package com.orbit.internsapi.dto;

import com.orbit.internsapi.entity.Intern;
import com.orbit.internsapi.entity.InternStatus;

import java.time.LocalDate;

public record InternResponse(
        Long id,
        String firstName,
        String lastName,
        String email,
        String university,
        LocalDate startDate,
        InternStatus status
) {
    public static InternResponse from(Intern intern) {
        return new InternResponse(
                intern.getId(),
                intern.getFirstName(),
                intern.getLastName(),
                intern.getEmail(),
                intern.getUniversity(),
                intern.getStartDate(),
                intern.getStatus()
        );
    }
}
